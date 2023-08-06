"""This module implements the SRMP algorithm,
as well as the preference elicitation algorithm and plot functions.

Implementation and naming conventions are taken from
:cite:p:`olteanu2022preference`.
"""
from itertools import permutations
from typing import Any, Dict, List, Optional, Tuple, cast

import numpy as np
from pandas import DataFrame, Series, concat
from pulp import (
    LpBinary,
    LpContinuous,
    LpMaximize,
    LpProblem,
    LpVariable,
    lpSum,
)
from pulp import value as pulp_value

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.relations import (
    IndifferenceRelation,
    OutrankingMatrix,
    PreferenceRelation,
    PreferenceStructure,
    Ranking,
)

from ..core.aliases import Function
from ..core.interfaces import Trainer
from ..core.scales import (
    PreferenceDirection,
    QualitativeScale,
    QuantitativeScale,
    Scale,
    is_better_or_equal,
)
from ..plot.plot import (
    Annotation,
    AreaPlot,
    Axis,
    BarPlot,
    Figure,
    HorizontalStripes,
    LinePlot,
    ParallelCoordinatesPlot,
    StackedBarPlot,
    Text,
)


class SubSRMP:
    """This class infers outranking relations related to a single category
    profile.

    The relation compares each criterion of each alternative values with the
    category profile (``1`` if better or equal, ``0`` otherwise), apply
    the `criteria_weights` as a weighted sum for each alternative and compare
    those scores.

    :param criteria_weights:
    :param category_profile:

    .. todo:: Find a better name
    """

    def __init__(
        self, criteria_weights: Dict[Any, float], category_profile: ScaleValues
    ):
        self.criteria_weights = criteria_weights
        self.category_profile = category_profile

    def construct(
        self, performance_table: PerformanceTable
    ) -> OutrankingMatrix:
        """Construct the outranking matrix.

        :param performance_table:
        ;return:
        """
        functions = {
            criterion: (
                cast(
                    Function,
                    lambda x, c=criterion: is_better_or_equal(
                        x,
                        self.category_profile.data[c],
                        cast(QuantitativeScale, performance_table.scales[c]),
                    ),
                )
            )  # https://bugs.python.org/issue13652
            for criterion in performance_table.criteria
        }

        conditional_weighted_sum = cast(
            Series,
            performance_table.apply_criteria_functions(functions)
            .apply_criteria_weights(self.criteria_weights)
            .sum(1),
        )

        return OutrankingMatrix(
            DataFrame(
                [
                    [
                        conditional_weighted_sum[ai]
                        >= conditional_weighted_sum[aj]
                        for aj in performance_table.alternatives
                    ]
                    for ai in performance_table.alternatives
                ],
                index=performance_table.alternatives,
                columns=performance_table.alternatives,
                dtype="int64",
            )
        )

    def __call__(
        self, performance_table: PerformanceTable
    ) -> OutrankingMatrix:
        """Construct an outranking matrix.

        :param performance_table:
        ;return:
        """
        return self.construct(performance_table=performance_table)


class SRMP:
    """This class implements the SRMP algorithm.

    :param criteria_weights:
    :param category_profiles:
    :param lexicographic_order: profile indices used sequentially to rank
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        category_profiles: PerformanceTable,
        lexicographic_order: List[int],
    ):
        self.criteria_weights = criteria_weights
        self.category_profiles = category_profiles
        self.lexicographic_order = lexicographic_order

    @property
    def sub_srmp(self) -> List[SubSRMP]:
        """Return list of sub SRMP problems (one per category profile).

        :return:
        """
        return [
            SubSRMP(
                self.criteria_weights,
                self.category_profiles.get_alternative_values(category),
            )
            for category in self.category_profiles.alternatives
        ]

    def construct(
        self, performance_table: PerformanceTable
    ) -> List[OutrankingMatrix]:
        """Construct one outranking matrix per category profile.

        :param performance_table:
        :return:
        """
        return [sub_srmp(performance_table) for sub_srmp in self.sub_srmp]

    def exploit(
        self,
        outranking_matrices: List[OutrankingMatrix],
        lexicographic_order: List[int] = None,
    ) -> Ranking:
        """Merge outranking matrices built by category profile in lexicographic
        order using SRMP exploitation method.

        :param outranking_matrices:
            outranking matrix constructed in :attr:`category_profiles` order
        :param lexicographic_order: (if not supplied, use attribute)
        :return:
            the outranking total order as a ranking
        """
        lexicographic_order = (
            self.lexicographic_order
            if lexicographic_order is None
            else lexicographic_order
        )
        relations_ordered = [
            outranking_matrices[i] for i in lexicographic_order
        ]
        n = len(relations_ordered)
        score = sum(
            [relations_ordered[i].df * 2 ** (n - 1 - i) for i in range(n)],
            DataFrame(
                0,
                index=relations_ordered[0].vertices,
                columns=relations_ordered[0].vertices,
            ),
        )
        outranking_matrix = score - score.transpose() >= 0
        scores = outranking_matrix.sum(1)
        scores_ordered = sorted(set(scores.values), reverse=True)
        return Ranking(
            scores.apply(lambda x: scores_ordered.index(x) + 1),
        )

    def __call__(self, performance_table: PerformanceTable) -> Ranking:
        """Compute the SRMP algorithm

        :param performance_table:
        :return:
            the outranking total order as a ranking
        """
        return self.exploit(self.construct(performance_table))

    @classmethod
    def train(
        cls,
        performance_table: PerformanceTable,
        relations: PreferenceStructure,
        max_profiles_number: int = None,
        profiles_number: int = None,
        lexicographic_order: List[int] = None,
        inconsistencies: bool = True,
        gamma: float = 0.001,
        non_dictator: bool = False,
        solver_args: dict = None,
    ) -> Optional["SRMP"]:
        """Train a SRMP instance

        :param performance_table:
        :param relations:
        :param max_profiles_number: highest number of reference profiles
        :param profiles_number: number of reference profiles
        :param lexicographic_order: profile indices used sequentially to rank
        :param inconsistencies:
            if ``True`` inconsistent comparisons will be taken into account
        :param gamma: value used for modeling strict inequalities
        :param non_dictator: if ``True`` prevent dictator weights (> 0.5)
        :param solver_args: extra arguments supplied to the solver
        :return: the inferred SRMP object
        :raise TypeError:
            * if `max_profiles_number`, `profiles_number`
              and `lexicographic_order` are not specified
            * if two or more of `max_profiles_number`, `profiles_number`
              and `lexicographic_order` are specified at the same time

        .. note::
            One and only one of `max_profiles_number`, `profiles_number`
            and `lexicographic_order` must be specified
        """
        return SRMPTrainer(
            performance_table,
            relations,
            max_profiles_number,
            profiles_number,
            lexicographic_order,
            inconsistencies,
            gamma,
            non_dictator,
            solver_args,
        ).train()

    @staticmethod
    def plot_input_data(
        performance_table: PerformanceTable,
        srmp: "SRMP" = None,
        criteria_weights: Dict[Any, float] = None,
        category_profiles: PerformanceTable = None,
        lexicographic_order: List[int] = None,
        annotations: bool = False,
        annotations_alpha: float = 0.5,
        scales_boundaries: bool = False,
        figsize: Tuple[float, float] = None,
        xticklabels_tilted: bool = False,
        **kwargs,
    ):  # pragma: nocover
        """Visualize input data.

        For each criterion, the arrow indicates the preference direction.
        The criteria weights are displayed as a bar plot,
        and their values are written in parentheses

        :param performance_table:
        :param srmp: a SRMP object (if given, overrides SRMP parameters)
        :param criteria_weights:
        :param category_profiles:
        :param lexicographic_order: profile indices used sequentially to rank
        :param annotations:
            if ``True`` every point is annotated with its value
        :param annotations_alpha: annotations white box transparency
        :param scales_boundaries:
            if ``True`` the criteria boundaries are the scales boundaries,
            else they are computed from the data
        :param figsize: figure size in inches as a tuple (`width`, `height`)
        :param xticklabels_tilted:
            if ``True`` `xticklabels` are tilted to better fit
        """
        # Reorder scales and criteria_weights
        scales = {
            crit: performance_table.scales[crit]
            for crit in performance_table.criteria
        }

        if srmp is not None:
            criteria_weights = srmp.criteria_weights
            category_profiles = srmp.category_profiles
            lexicographic_order = srmp.lexicographic_order

        if criteria_weights is not None:
            criteria_weights = {
                crit: criteria_weights[crit]
                for crit in performance_table.criteria
            }

        # Transform to quantitative scales
        quantitative_scales = {}
        for key, scale in scales.items():
            if isinstance(scale, QualitativeScale):
                quantitative_scales[key] = scale.quantitative
            else:
                quantitative_scales[key] = cast(QuantitativeScale, scale)

        # Concatenate category_profiles with performance_table
        if category_profiles is not None:
            df = concat([performance_table.df, category_profiles.df])
        else:
            df = performance_table.df.copy()
        table = PerformanceTable(df, scales=scales)
        table = table.transform(cast(Dict[str, Scale], quantitative_scales))
        if not scales_boundaries:
            table.scales = table.bounds
            # Conserve preference direction
            for key, scale in quantitative_scales.items():
                cast(
                    QuantitativeScale, table.scales[key]
                ).preference_direction = scale.preference_direction
        table = table.normalize()

        # Create constants
        nb_alt = len(performance_table.alternatives)
        if category_profiles is not None:
            nb_profiles = len(category_profiles.alternatives)

        # Create figure and axis
        fig = Figure(figsize=figsize)
        ax = fig.create_add_axis()

        # Axis parameters
        x = cast(List[float], range(len(performance_table.criteria)))
        xticks = cast(List[float], (range(len(performance_table.criteria))))
        if criteria_weights is not None:
            xticklabels = [
                f"{crit}\n({weight})"
                for crit, weight in criteria_weights.items()
            ]
        else:
            xticklabels = [f"{crit}" for crit in performance_table.criteria]

        # Criteria weights
        if criteria_weights is not None:
            weights = np.array([*criteria_weights.values()])
            weights_normalized = weights / weights.sum()
            ax.add_plot(
                BarPlot(
                    x,
                    weights_normalized,
                    xticks=xticks,
                    yticks=[],
                    xticklabels=xticklabels,
                    xticklabels_tilted=xticklabels_tilted,
                    width=0.1,
                    alpha=0.5,
                )
            )

        # Plotted annotations' coordinates
        annotations_coord: List[Tuple[float, float]] = []

        # Profiles
        if category_profiles is not None:
            for profile in range(nb_alt, nb_alt + nb_profiles):
                ax.add_plot(
                    AreaPlot(
                        x,
                        table.df.iloc[profile],
                        xticks=xticks,
                        yticks=[],
                        xticklabels=xticklabels,
                        xticklabels_tilted=xticklabels_tilted,
                        color="black",
                        alpha=0.1,
                        strongline=False,
                    )
                )
                ax.add_plot(
                    Annotation(
                        0,
                        table.df.iloc[profile, 0],
                        f"$P^{profile - nb_alt}$",
                        -1,
                        0,
                        "right",
                        "center",
                    )
                )

        # Alternatives
        values = table.df[:nb_alt]
        labels = table.df[:nb_alt].index
        ax.add_plot(
            ParallelCoordinatesPlot(
                x,
                values,
                xticks=xticks,
                yticks=[],
                xticklabels=xticklabels,
                xticklabels_tilted=xticklabels_tilted,
                labels=labels,
                linestyle="-.",
            )
        )
        # Legend
        ax.add_legend(title="Alternatives :", location="right")

        fig.draw()
        assert ax.ax is not None  # to comply with mypy

        # Annotations
        if annotations:
            if category_profiles is not None:
                for profile in range(nb_alt, nb_alt + nb_profiles):
                    for i in x:
                        xy = (i, table.df.iloc[profile, i])
                        overlap = False
                        for (xc, yc) in annotations_coord:
                            if (xc == i) and (
                                abs(
                                    ax.ax.transData.transform(xy)[1]
                                    - ax.ax.transData.transform((xc, yc))[1]
                                )
                                < 20
                            ):
                                # if current annotation overlaps
                                # already plotted annotations
                                overlap = True
                                break

                        if not overlap:
                            annotation = Annotation(
                                i,
                                table.df.iloc[profile, i],
                                category_profiles.df.iloc[profile - nb_alt, i],
                                2,
                                0,
                                "left",
                                "center",
                                annotations_alpha,
                            )
                            ax.add_plot(annotation)
                            annotations_coord.append(
                                (i, table.df.iloc[profile, i])
                            )

            for alt in range(nb_alt):
                for i in x:
                    xy = (i, table.df.iloc[alt, i])
                    overlap = False
                    for (xc, yc) in annotations_coord:
                        if (xc == i) and (
                            abs(
                                ax.ax.transData.transform(xy)[1]
                                - ax.ax.transData.transform((xc, yc))[1]
                            )
                            < 20
                        ):
                            # if current annotation overlaps
                            # already plotted annotations
                            overlap = True
                            break

                    if not overlap:
                        annotation = Annotation(
                            i,
                            table.df.iloc[alt, i],
                            performance_table.df.iloc[alt, i],
                            2,
                            0,
                            "left",
                            "center",
                            annotations_alpha,
                        )
                        ax.add_plot(annotation)
                        annotations_coord.append((i, table.df.iloc[alt, i]))

        # Lexicographic order
        if lexicographic_order is not None:
            text = Text(
                0,
                1.2,
                "Lexicographic order : $"
                + r" \rightarrow ".join(
                    [f"P^{profile}" for profile in lexicographic_order]
                )
                + "$",
                box=True,
            )
            ax.add_plot(text)
        fig.draw()

    def plot_concordance_index(
        self,
        performance_table: PerformanceTable,
        figsize: Tuple[float, float] = None,
        ncols: int = 0,
        nrows: int = 0,
        xlabels_tilted: bool = False,
        **kwargs,
    ):  # pragma: nocover
        """Visualize concordance index between alternatives and profiles

        :param performance_table:
        :param figsize: figure size in inches as a tuple (`width`, `height`)
        :param xlabels_tilted:
            if ``True`` `xlabels` are tilted to better fit
        """
        # Create constants
        nb_alt = len(performance_table.alternatives)
        nb_profiles = len(self.category_profiles.alternatives)
        weights_sum = sum(self.criteria_weights.values())

        # Create figure and axes
        fig = Figure(figsize=figsize, ncols=ncols, nrows=nrows)

        for ind_alt in range(nb_alt):
            ax = Axis(
                xlabel=f"{performance_table.df.index[ind_alt]}",
                xlabel_tilted=xlabels_tilted,
            )
            # Axis properties
            x = cast(List[float], range(nb_profiles))
            xticks = cast(List[float], range(nb_profiles))
            xticklabels = [
                f"$P^{profile}$" for profile in self.lexicographic_order
            ]
            ylim = (0.0, 1.0)

            values = []
            # Draw the stacked barplot
            for ind_crit, crit in enumerate(performance_table.criteria):
                crit_values = [
                    self.criteria_weights[crit] / weights_sum
                    if is_better_or_equal(
                        performance_table.df.iloc[ind_alt, ind_crit],
                        self.category_profiles.df.iloc[profile, ind_crit],
                        cast(
                            QuantitativeScale,
                            performance_table.scales[crit],
                        ),
                    )
                    else 0
                    for profile in self.lexicographic_order
                ]
                values.append(crit_values)
            ax.add_plot(
                StackedBarPlot(
                    x,
                    values,
                    ylim=ylim,
                    xticks=xticks,
                    xticklabels=xticklabels,
                    labels=cast(
                        List[Optional[Any]], performance_table.criteria
                    ),
                )
            )
            fig.add_axis(ax)
        ax.add_legend(title="Criteria :", location="right")
        fig.draw()

    def plot_progressive_ranking(
        self,
        performance_table: PerformanceTable,
        figsize: Tuple[float, float] = None,
        **kwargs,
    ):  # pragma: nocover
        """Visualize ranking progressively according to the lexicographic order

        :param performance_table:
        :param figsize: figure size in inches as a tuple (`width`, `height`)
        """
        # Create constants
        nb_alt = len(performance_table.alternatives)
        nb_profiles = len(self.lexicographic_order)

        # Compute rankings progressively
        relations = self.construct(performance_table)
        rankings = DataFrame(
            [
                self.exploit(relations, self.lexicographic_order[:stop]).data
                for stop in range(1, nb_profiles + 1)
            ]
        )

        # Compute ranks
        final_values = (
            rankings.iloc[nb_profiles - 1].drop_duplicates().sort_values()
        )
        value_to_rank = {
            value: rank
            for value, rank in zip(
                final_values, range(1, len(final_values) + 1)
            )
        }
        ranks = rankings.applymap(lambda x: value_to_rank[x])
        nb_ranks = len(value_to_rank)

        # Create figure and axes
        fig = Figure(figsize=figsize)
        ax = Axis(xlabel="Profiles", ylabel="Rank")
        fig.add_axis(ax)

        # Axis parameters
        xticks = cast(List[float], range(nb_profiles))
        xticklabels = [
            f"$P^{profile}$" for profile in self.lexicographic_order
        ]
        ylim = (0.5, nb_ranks + 0.5)
        yticks = cast(List[float], range(1, nb_ranks + 1))
        yminorticks = np.arange(1, nb_ranks + 2) - 0.5
        yticklabels = cast(List[str], range(nb_ranks, 0, -1))

        # Draw horizontal striped background
        ax.add_plot(
            HorizontalStripes(
                yminorticks.tolist(),
                color="black",
                alpha=0.1,
                attach_yticks=True,
            )
        )

        # Number of alternatives for each rank (depending on the profile)
        rank_counts = DataFrame(
            [
                {
                    k: v
                    for k, v in zip(
                        *np.unique(ranks.loc[profile], return_counts=True)
                    )
                }
                for profile in ranks.index
            ],
            columns=range(1, nb_alt + 1),
        ).fillna(0)
        # Offsets' width for each rank (depending on the profile)
        offsets_width = 1 / (rank_counts + 1)
        # Offsets to apply to current alternative's ranks
        offsets = [0.5] * nb_profiles
        # Alternatives sorted according to the final ranking
        final_ranking_sorted = (
            rankings.iloc[-1].sort_values(ascending=False).index
        )
        # Previous alternative's ranks
        previous_ranks = [0] * nb_profiles

        for alt in final_ranking_sorted:
            # Current alternative's ranks
            current_ranks = ranks[alt]
            # Update offsets (return to 0.5 if it's a new rank)
            offsets = np.where(
                current_ranks == previous_ranks, offsets, 0.5
            ).tolist()
            offsets = [
                offsets[profile]
                - offsets_width.loc[profile, current_ranks[profile]]
                for profile in range(nb_profiles)
            ]
            x = cast(List[float], range(nb_profiles))
            y = current_ranks + offsets
            ax.add_plot(
                LinePlot(
                    x,
                    y,
                    xticks=xticks,
                    xticklabels=xticklabels,
                    ylim=ylim,
                    yticks=yticks,
                    yticklabels=yticklabels,
                    marker="o",
                )
            )
            ax.add_plot(
                Annotation(
                    nb_profiles - 1,
                    current_ranks.iloc[-1] + offsets[-1],
                    str(alt),
                    10,
                    0,
                    vertical_alignement="center",
                    box=True,
                )
            )
            previous_ranks = current_ranks
        fig.draw()


class SRMPTrainer(Trainer[Optional[SRMP]]):
    """This class gathers functions used to train a SRMP model.

    :param performance_table:
    :param relations:
    :param max_profiles_number: highest number of reference profiles
    :param profiles_number: number of reference profiles
    :param lexicographic_order: profile indices used sequentially to rank
    :param inconsistencies:
        if ``True`` inconsistent comparisons will be taken into account
    :param gamma: value used for modeling strict inequalities
    :param non_dictator: if ``True`` prevent dictator weights (> 0.5)
    :param solver_args: extra arguments supplied to the solver
    :raise TypeError:
        * if `max_profiles_number`, `profiles_number`
          and `lexicographic_order` are not specified

    .. note::
        If multiple arguments are supplied, only one will be used in the
        following priority: `lexicographic_order`, `profiles_number` then
        `max_profiles_number`
    """

    def __init__(
        self,
        performance_table: PerformanceTable,
        relations: PreferenceStructure,
        max_profiles_number: int = None,
        profiles_number: int = None,
        lexicographic_order: List[int] = None,
        inconsistencies: bool = True,
        gamma: float = 0.001,
        non_dictator: bool = False,
        solver_args: dict = None,
    ):
        # Check parameters provided
        provided = (
            (max_profiles_number is not None)
            + (profiles_number is not None)
            + (lexicographic_order is not None)
        )
        if provided == 0:
            raise ValueError(
                "You must specify either 'max_profiles_number',\
                'profiles_number' or 'lexicographic_order'"
            )
        self.performance_table = performance_table
        self.relations = relations
        self.max_profiles_number = max_profiles_number
        self.profiles_number = profiles_number
        self.lexicographic_order = lexicographic_order
        self.inconsistencies = inconsistencies
        self.gamma = gamma
        self.non_dictator = non_dictator
        self.solver_args = {} if solver_args is None else solver_args
        self.problem = LpProblem("SRMP_Training", LpMaximize)

    @staticmethod
    def compute_fitness(
        problem: LpProblem, nb_relations: int, inconsistencies: bool = True
    ) -> float:
        """Compute fitness of a SRMP solution.

        :param problem: LP problem (solved)
        :param nb_relations: number of relations supplied for training
        :param inconsistencies:
            if ``True`` inconsistent comparisons will be taken into account
        """
        return (
            0
            if problem.status != 1
            else (
                pulp_value(problem.objective) / nb_relations
                if inconsistencies
                else 1
            )
        )

    @property
    def fitness(self) -> float:
        """Return fitness of last trained solution.

        :return:
        """
        return self.compute_fitness(
            self.problem, len(self.relations), self.inconsistencies
        )

    def _train_lexicographic_order(
        self, lexicographic_order: List[int]
    ) -> Tuple[Optional[SRMP], LpProblem]:
        """Train a SRMP instance using lexicographic order

        :param lexicographic_order: profile indices used sequentially to rank
        :return: the inferred SRMP object, along its LP problem
        """
        performance_table = self.performance_table.normalize()

        ##############
        # Parameters #
        ##############

        # List of alternatives
        A_star = self.relations.elements
        # List of criteria
        M = self.performance_table.criteria
        # Number of profiles
        k = len(lexicographic_order)
        # Indices of profiles
        profile_indices = list(range(1, k + 1))
        # Lexicographic order
        sigma = [0] + [profile + 1 for profile in lexicographic_order]
        # Binary comparisons with preference
        preference_relations = PreferenceStructure(
            self.relations[PreferenceRelation]
        )
        preference_relations_indices = range(len(preference_relations))
        # Binary comparisons with indifference
        indifference_relations = PreferenceStructure(
            self.relations[IndifferenceRelation]
        )
        indifference_relations_indices = range(len(indifference_relations))

        #############
        # Variables #
        #############

        # Weights
        w = LpVariable.dicts(
            "Weight", M, lowBound=0, upBound=1, cat=LpContinuous
        )
        # Reference profiles
        p = LpVariable.dicts("Profile", (profile_indices, M), cat=LpContinuous)
        # Local concordance to a reference point
        delta = LpVariable.dicts(
            "LocalConcordance",
            (A_star, profile_indices, M),
            cat=LpBinary,
        )
        # Weighted local concordance to a reference point
        omega = LpVariable.dicts(
            "WeightedLocalConcordance",
            (A_star, profile_indices, M),
            lowBound=0,
            upBound=1,
            cat=LpContinuous,
        )
        # Variables used to model the ranking rule with preference relations
        s = LpVariable.dicts(
            "PreferenceRankingVariable",
            (
                preference_relations_indices,
                [0] + profile_indices,
            ),
            cat=LpBinary,
        )

        if self.inconsistencies:
            # Variables used to model the ranking rule with indifference
            # relations
            s_star = LpVariable.dicts(
                "IndifferenceRankingVariable",
                indifference_relations_indices,
                cat=LpBinary,
            )

        ##############
        # LP problem #
        ##############

        prob = LpProblem("SRMP_Elicitation", LpMaximize)

        if self.inconsistencies:
            prob += lpSum(
                [s[index][0] for index in preference_relations_indices]
            ) + lpSum(
                [s_star[index] for index in indifference_relations_indices]
            )

        ###############
        # Constraints #
        ###############

        # Normalized weights
        prob += lpSum([w[j] for j in M]) == 1

        for j in M:
            if self.non_dictator:
                # Non-dictator weights
                prob += w[j] <= 0.5

            # Non-zero weights
            prob += w[j] >= self.gamma

            # Constraints on the reference profiles
            prob += p[1][j] >= 0
            prob += p[k][j] <= 1

            for h in profile_indices:
                if h != k:
                    # Dominance between the reference profiles
                    prob += p[h + 1][j] >= p[h][j]

                for a in A_star:
                    # Constraints on the local concordances
                    prob += (
                        performance_table.df.loc[a, j] - p[h][j]
                        >= delta[a][h][j] - 1
                    )
                    prob += (
                        delta[a][h][j]
                        >= performance_table.df.loc[a, j]
                        - p[h][j]
                        + self.gamma
                    )

                    # Constraints on the weighted local concordances
                    prob += omega[a][h][j] <= w[j]
                    prob += omega[a][h][j] >= 0
                    prob += omega[a][h][j] <= delta[a][h][j]
                    prob += omega[a][h][j] >= delta[a][h][j] + w[j] - 1

        # Constraints on the preference ranking variables
        for index in preference_relations_indices:
            if not self.inconsistencies:
                prob += s[index][sigma[0]] == 1
            prob += s[index][sigma[k]] == 0

        for h in profile_indices:
            # Constraints on the preferences
            for index, relation in enumerate(preference_relations):
                a, b = relation.a, relation.b

                prob += lpSum([omega[a][sigma[h]][j] for j in M]) >= (
                    lpSum([omega[b][sigma[h]][j] for j in M])
                    + self.gamma
                    - s[index][sigma[h]] * (1 + self.gamma)
                    - (1 - s[index][sigma[h - 1]])
                )

                prob += lpSum([omega[a][sigma[h]][j] for j in M]) >= (
                    lpSum([omega[b][sigma[h]][j] for j in M])
                    - (1 - s[index][sigma[h]])
                    - (1 - s[index][sigma[h - 1]])
                )

                prob += lpSum([omega[a][sigma[h]][j] for j in M]) <= (
                    lpSum([omega[b][sigma[h]][j] for j in M])
                    + (1 - s[index][sigma[h]])
                    + (1 - s[index][sigma[h - 1]])
                )

            # Constraints on the indifferences
            for index, relation in enumerate(indifference_relations):
                a, b = relation.a, relation.b
                if not self.inconsistencies:
                    prob += lpSum([omega[a][sigma[h]][j] for j in M]) == lpSum(
                        [omega[b][sigma[h]][j] for j in M]
                    )
                else:
                    prob += lpSum([omega[a][sigma[h]][j] for j in M]) <= (
                        lpSum([omega[b][sigma[h]][j] for j in M])
                        - (1 - s_star[index])
                    )

                    prob += lpSum([omega[b][sigma[h]][j] for j in M]) <= (
                        lpSum([omega[a][sigma[h]][j] for j in M])
                        - (1 - s_star[index])
                    )

        # Solve problem
        status = prob.solve(**self.solver_args)

        if status != 1:
            return None, prob

        # Compute optimum solution
        criteria_weights = {j: pulp_value(w[j]) for j in M}
        profiles = PerformanceTable(
            [[pulp_value(p[h][j]) for j in M] for h in profile_indices],
            criteria=M,
        )
        # Denormalize profile values
        profiles = self._denormalize(
            profiles,
            cast(Dict[Any, QuantitativeScale], self.performance_table.scales),
        )

        return SRMP(criteria_weights, profiles, lexicographic_order), prob

    def _train(
        self,
        lexicographic_order: List[int] = None,
        profiles_number: int = None,
        max_profiles_number: int = None,
    ) -> Tuple[Optional[SRMP], LpProblem]:
        """Train a SRMP instance

        :param lexicographic_order: profile indices used sequentially to rank
        :param profiles_number: number of reference profiles
        :param max_profiles_number: highest number of reference profiles
        :return: the inferred SRMP object, along with its fitness
        :raise TypeError:
            * if `max_profiles_number`, `profiles_number` and
              `lexicographic_order` are not specified

        .. note::
            If multiple arguments are supplied, only one will be used in the
            following priority: `lexicographic_order`, `profiles_number` then
            `max_profiles_number`
        """
        # Check parameters provided
        provided = (
            (max_profiles_number is not None)
            + (profiles_number is not None)
            + (lexicographic_order is not None)
        )
        if provided == 0:
            raise ValueError(
                "You must specify either 'max_profiles_number',\
                'profiles_number' or 'lexicographic_order'"
            )
        if lexicographic_order is not None:
            # Compute the training algorithm
            result, prob = self._train_lexicographic_order(lexicographic_order)
            return result, prob
        if profiles_number is not None:
            lexicographic_order_list = list(
                permutations(range(profiles_number))
            )
            best_result = None
            best_prob = None
            best_fitness = -1.0
            for current_lexicographic_order in lexicographic_order_list:
                # Compute the training algorithm for each lexicographic order
                result, prob = self._train(
                    lexicographic_order=list(current_lexicographic_order),
                )
                fitness = self.compute_fitness(
                    prob, len(self.relations), self.inconsistencies
                )

                if fitness > best_fitness:
                    best_result = result
                    best_prob = prob
                    best_fitness = fitness
                if best_fitness == 1:
                    # Break recursion when a perfect solution is found
                    break
            return best_result, best_prob

        profiles_number_list = (
            list(range(1, max_profiles_number + 1))
            if max_profiles_number is not None
            else []
        )

        best_result = None
        best_prob = None
        best_fitness = -1.0
        for profiles_number in profiles_number_list:
            # Compute the training algorithm for each profiles number
            result, prob = self._train(
                profiles_number=profiles_number,
            )
            fitness = self.compute_fitness(
                prob, len(self.relations), self.inconsistencies
            )
            if fitness > best_fitness:
                best_result = result
                best_fitness = fitness
                best_prob = prob
            if best_fitness == 1:
                # Break recursion when a perfect solution is found
                break
        return best_result, best_prob

    def train(self) -> Optional[SRMP]:
        """Train and return SRMP solution (if existing).

        :return:
        """
        result, self.problem = self._train(
            self.lexicographic_order,
            self.profiles_number,
            self.max_profiles_number,
        )
        return result

    @staticmethod
    def _denormalize_value(
        x: float,
        scale: QuantitativeScale,
    ) -> Any:
        """Denormalize value by taking the closest preferred value available

        :param x:
        :param scale:
        :return:
        """
        if isinstance(scale, QualitativeScale):
            denormalized_x = cast(
                float,
                QuantitativeScale.normal().transform_to(x, scale.quantitative),
            )
            closest_prefered_value = (
                min(
                    [
                        value
                        for value in scale.values
                        if value >= denormalized_x
                    ]
                )
                if scale.preference_direction == PreferenceDirection.MAX
                else max(
                    [
                        value
                        for value in scale.values
                        if value <= denormalized_x
                    ]
                )
            )
            return scale.label_from_value(closest_prefered_value)
        else:
            return QuantitativeScale.normal().transform_to(x, scale)

    @staticmethod
    def _denormalize(
        performance_table: PerformanceTable,
        scales: Dict[str, QuantitativeScale],
    ) -> PerformanceTable:
        """Denormalize performance table with the closest preferred values
        available

        :param performance_table:
        :param scales: target criteria scales
        :return: denormalized performance table
        """
        functions = {
            criterion: (
                cast(
                    Function,
                    lambda x, c=criterion: SRMPTrainer._denormalize_value(
                        x, scales[c]
                    ),
                )
            )  # https://bugs.python.org/issue13652
            for criterion in scales.keys()
        }
        res = performance_table.apply_criteria_functions(functions)
        res.scales = cast(Dict[Any, Scale], scales)
        return res
