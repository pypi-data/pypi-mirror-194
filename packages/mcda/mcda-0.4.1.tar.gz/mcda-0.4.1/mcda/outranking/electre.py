"""This module implements the Electre algorithms.

Implementation and naming conventions are taken from
:cite:p:`vincke1998electre`.
"""
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Dict, List, Tuple, cast

from pandas import DataFrame, Series

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    OutrankingMatrix,
    PreferenceRelation,
    Relation,
)
from mcda.core.scales import PreferenceDirection, QuantitativeScale


class Electre(ABC):
    """This class represents the interface for Electre algorithms.

    :param criteria_weights:
    """

    def __init__(self, criteria_weights: Dict[Any, float]):
        self.criteria_weights = criteria_weights

    def _pairwise_concordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Compute the concordance comparison of 2 alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :param scales:
        :return: concordance index

        .. warning::
            this method assumes that alternatives values have the same scales
        """
        scales = cast(Dict[str, QuantitativeScale], alternative_values1.scales)
        concordance_value = 0.0
        for k in alternative_values1.labels:
            concordance_value = (
                concordance_value + self.criteria_weights[k]
                if (
                    alternative_values1[k] >= alternative_values2[k]
                    and scales[k].preference_direction
                    == PreferenceDirection.MAX
                )
                or (
                    alternative_values1[k] <= alternative_values2[k]
                    and scales[k].preference_direction
                    == PreferenceDirection.MIN
                )
                else concordance_value
            )
        concordance_value = concordance_value / sum(
            self.criteria_weights.values()
        )
        assert concordance_value >= 0
        return concordance_value

    def concordance(
        self,
        performance_table: PerformanceTable,
    ) -> DataFrame:
        """Compute the concordance matrix.

        :param performance_table:
        :return: concordance matrix
        """
        return DataFrame(
            [
                [
                    self._pairwise_concordance(
                        performance_table.get_alternative_values(ai),
                        performance_table.get_alternative_values(aj),
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            index=performance_table.alternatives,
            columns=performance_table.alternatives,
        )

    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> DataFrame:
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix
        """
        pref_factor = Series(
            {
                c: (
                    1
                    if scale.preference_direction == PreferenceDirection.MAX
                    else -1
                )
                for c, scale in cast(
                    Dict[Any, QuantitativeScale], performance_table.scales
                ).items()
            }
        )
        return DataFrame(
            [
                [
                    max(
                        (
                            performance_table.get_alternative_values(aj).data
                            - performance_table.get_alternative_values(ai).data
                        )
                        * pref_factor
                    )
                    for aj in performance_table.alternatives
                ]
                for ai in performance_table.alternatives
            ],
            index=performance_table.alternatives,
            columns=performance_table.alternatives,
        ) / max(performance_table.df.apply(lambda x: max(x) - min(x)))

    @abstractmethod
    def __call__(
        self, performance_table: PerformanceTable, **kwargs
    ) -> Any:  # pragma: nocover
        """Apply the chosen Electre algorithm.

        :param performance_table:
        :return: outranking matrix
        """
        pass


class Electre1(Electre):
    """This class implements the Electre I algorithm.

    :param criteria_weights:
    :param c_hat: concordance threshold
    :param d_hat: discordance threshold
    """

    def __init__(
        self, criteria_weights: Dict[Any, float], c_hat: float, d_hat: float
    ):
        super().__init__(criteria_weights)
        self.c_hat = c_hat
        self.d_hat = d_hat

    def outranking(
        self,
        concordance_matrix: DataFrame,
        discordance_matrix: DataFrame,
    ) -> OutrankingMatrix:
        """Compute the outranking matrix using Electre I method.

        :param concordance_matrix: concordance matrix
        :param discordance_matrix: discordance matrix
        :return: the outranking matrix
        """
        ones = DataFrame(
            1,
            index=concordance_matrix.index,
            columns=concordance_matrix.columns,
        )
        return OutrankingMatrix(
            ones[
                (concordance_matrix >= self.c_hat)
                & (discordance_matrix <= self.d_hat)
            ].fillna(0)
        )

    def construct(
        self, performance_table: PerformanceTable
    ) -> OutrankingMatrix:
        """Construct the outranking matrix using Electre I method.

        :param performance_table:
        :return: the outranking matrix of the performance table
        """
        return self.outranking(
            self.concordance(performance_table),
            self.discordance(performance_table),
        )

    def exploit(
        self,
        outranking_matrix: OutrankingMatrix,
        cycle_reduction: bool = False,
        transitivity: bool = False,
    ) -> List:
        """Choose best alternative candidates from outranking matrix.

        It uses :meth:`OutrankingMatrix.kernel` to find the best candidates.

        :param outranking_matrix:
        :param cycle_reduction:
            if ``True``, apply :attr:`.AdjacencyMatrix.cycle_reduction_matrix`
            to outranking matrix
        :param transitivity:
            if ``True``, apply :attr:`.AdjacencyMatrix.transitive_closure` to
            outranking matrix
        :return: best alternative candidates

        .. warning::
            if `outranking_matrix` kernel does not exist, it returns all
            alternatives
        """
        matrix = (
            outranking_matrix.cycle_reduction_matrix
            if cycle_reduction
            else outranking_matrix
        )
        matrix = matrix.transitive_closure if transitivity else matrix
        kernel = matrix.kernel
        return kernel if len(kernel) > 0 else outranking_matrix.vertices

    def __call__(
        self,
        performance_table: PerformanceTable,
        cycle_reduction: bool = False,
        transitivity: bool = False,
        **kwargs,
    ) -> List:
        """Compute the outranking matrix using Electre I method.

        :param performance_table:
        :param cycle_reduction:
            if ``True``, apply :attr:`.AdjacencyMatrix.cycle_reduction_matrix`
            to outranking matrix
        :param transitivity:
            if ``True``, apply :attr:`.AdjacencyMatrix.transitive_closure` to
            outranking matrix
        :return: best alternative candidates

        .. warning::
            if `outranking_matrix` kernel does not exist, it returns all
            alternatives
        """
        matrix = self.construct(performance_table)
        return self.exploit(
            matrix, cycle_reduction=cycle_reduction, transitivity=transitivity
        )


class Electre2(Electre):
    """This class implements the Electre II algorithm.

    :param criteria_weights:
    :param c_hat: concordance thresholds (min, max)
    :param d_hat: discordance threshold (min, max)
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        c_hat: Tuple[float, float],
        d_hat: Tuple[float, float],
    ):
        Electre.__init__(self, criteria_weights)
        self.c_hat: Tuple[float, float] = c_hat
        self.d_hat: Tuple[float, float] = d_hat

    def outranking(
        self,
        concordance_matrix: DataFrame,
        discordance_matrix: DataFrame,
        c_hat: float = None,
        d_hat: float = None,
    ) -> OutrankingMatrix:
        """Calculate the outranking matrix according to given thresholds.

        :param concordance_matrix: concordance matrix
        :param discordance_matrix: discordance matrix
        :param c_hat: concordance threshold
        :param d_hat: discordance threshold
        :return: outranking matrix
        """
        c_hat = self.c_hat[1] if c_hat is None else c_hat
        d_hat = self.d_hat[0] if d_hat is None else d_hat
        ones = DataFrame(
            1,
            index=concordance_matrix.index,
            columns=concordance_matrix.columns,
        )
        return OutrankingMatrix(
            ones[
                (concordance_matrix >= concordance_matrix.T)
                & (concordance_matrix >= c_hat)
                & (discordance_matrix <= d_hat)
            ].fillna(0)
        )

    @staticmethod
    def distillation(
        strong_outranking_matrix: OutrankingMatrix,
        weak_outranking_matrix: OutrankingMatrix,
        ascending: bool = False,
    ) -> List[List[Any]]:
        """Compute distillation using outranking matrices.

        :param strong_outranking_matrix:
        :param weak_outranking_matrix:
        :param ascending:
            if ``True`` distillation is done in ascending direction
        :return: ranking of categories
        """
        axis = 1 if ascending else 0
        distillate = []
        rest = weak_outranking_matrix.vertices
        strong_outranking_matrix = cast(
            OutrankingMatrix, strong_outranking_matrix.cycle_reduction_matrix
        )
        weak_outranking_matrix = cast(
            OutrankingMatrix, weak_outranking_matrix.cycle_reduction_matrix
        )
        while len(rest) > 0:
            outranked = strong_outranking_matrix.df.loc[rest, rest].apply(
                sum, axis=axis
            )
            B = outranked[outranked == 0].index.tolist()
            outranked = weak_outranking_matrix.df.loc[B, B].apply(
                sum, axis=axis
            )
            A = outranked[outranked == 0].index.tolist()
            for i in A:
                rest.remove(i)
            distillate.append(A)
        return distillate[::-1] if ascending else distillate

    def construct(
        self, performance_table: PerformanceTable
    ) -> Tuple[OutrankingMatrix, OutrankingMatrix]:
        """Compute strong and weak dominance outranking matrices.

        :param performance_table:
        :return: strong outranking matrix, weak outranking matric
        """
        concordance_matrix = self.concordance(performance_table)
        discordance_matrix = self.discordance(performance_table)
        s_dominance_matrix = self.outranking(
            concordance_matrix,
            discordance_matrix,
            c_hat=self.c_hat[1],
            d_hat=self.d_hat[0],
        )
        w_dominance_matrix = self.outranking(
            concordance_matrix,
            discordance_matrix,
            c_hat=self.c_hat[0],
            d_hat=self.d_hat[1],
        )
        return s_dominance_matrix, w_dominance_matrix

    def exploit(
        self,
        strong_outranking_matrix: OutrankingMatrix,
        weak_outranking_matrix: OutrankingMatrix,
    ) -> OutrankingMatrix:
        """Compute distillations and merge results.

        :param strong_outranking_matrix:
        :param weak_outranking_matrix:
        :return: result outranking matrix
        """
        return OutrankingMatrix.from_ranked_categories(
            self.distillation(
                strong_outranking_matrix,
                weak_outranking_matrix,
                ascending=True,
            )
        ) * OutrankingMatrix.from_ranked_categories(
            self.distillation(
                strong_outranking_matrix,
                weak_outranking_matrix,
                ascending=False,
            )
        )

    def __call__(
        self, performance_table: PerformanceTable, **kwargs
    ) -> OutrankingMatrix:
        """Compute final outranking matrix for Electre II.

        :param performance_table:
        :return: result outranking matrix
        """
        return self.exploit(*self.construct(performance_table))


class Electre3(Electre):
    """This class implements the Electre III algorithm.

    :param criteria_weights:
    :param preference_thresholds:
    :param indifference_thresholds:
    :param veto_thresholds:
    :param alpha:  preset up values of distillation coefficients
    :param beta: preset up values of distillation coefficients
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        veto_thresholds: Dict[Any, float],
        alpha: float = 0.30,
        beta: float = -0.15,
    ):
        Electre.__init__(self, criteria_weights)
        self.preference_thresholds = preference_thresholds
        self.indifference_thresholds = indifference_thresholds
        self.veto_thresholds = veto_thresholds
        self.alpha = alpha
        self.beta = beta

    @staticmethod
    def _concordance_index(
        ga: float,
        gb: float,
        pga: float,
        qga: float,
        preference_direction: PreferenceDirection,
    ) -> float:
        """Compute the concordance index between two alternatives wrt a
        criterion.

        :param ga: preference function of first alternative wrt criterion
        :param gb: preference function of second alternative wrt criterion
        :param pga: preference threshold for the criterion
        :param qga: indifference threshold for the criterion
        :param preference_direction:
        :return: concordance index value"""
        if pga < qga:
            raise ValueError(
                "Indifference value cannot be greater than preference value"
            )
        if (
            gb > (ga + pga) and preference_direction == PreferenceDirection.MAX
        ) or (
            gb < (ga - pga) and preference_direction == PreferenceDirection.MIN
        ):
            return 0
        if (
            gb <= (ga + qga)
            and preference_direction == PreferenceDirection.MAX
        ) or (
            gb >= (ga - qga)
            and preference_direction == PreferenceDirection.MIN
        ):
            return 1
        return (
            (ga + pga - gb) / (pga - qga)
            if preference_direction == PreferenceDirection.MAX
            else (-ga + pga + gb) / (pga - qga)
        )

    def _pairwise_concordance(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Compute the pairwise concordance between two alternatives.

        :param alternative_values1:
        :param alternative_values2:
        :param scales:
        :return: pairwise concordance value

        .. warning::
            this method assumes that alternatives values have the same scales
        """

        scales = cast(Dict[str, QuantitativeScale], alternative_values1.scales)
        return sum(
            self.criteria_weights[i]
            * self._concordance_index(
                alternative_values1[i],
                alternative_values2[i],
                self.preference_thresholds[i],
                self.indifference_thresholds[i],
                scales[i].preference_direction,
            )
            for i in self.criteria_weights
        ) / sum(self.criteria_weights.values())

    @staticmethod
    def _discordance_index(
        ga: float,
        gb: float,
        pga: float,
        vga: float,
        preference_direction: PreferenceDirection,
    ) -> float:
        """Compute the discordance index between two alternatives wrt a
        criterion.

        :param ga: preference function of first alternative wrt the criterion
        :param gb: preference function of second alternative wrt the criterion
        :param pga: preference threshold for the criterion
        :param vga:
            veto threshold for the criterion. ``None`` for the highest value
        :param preference_direction:
        :return: discordance index value"""
        if vga is not None and pga > vga:
            raise ValueError(
                "Preference value cannot be greater than Veto value"
            )
        if (
            vga is None
            or (
                gb <= (ga + pga)
                and preference_direction == PreferenceDirection.MAX
            )
            or (
                gb >= (ga - pga)
                and preference_direction == PreferenceDirection.MIN
            )
        ):
            return 0
        elif (
            gb > (ga + vga) and preference_direction == PreferenceDirection.MAX
        ) or (
            gb < (ga - vga) and preference_direction == PreferenceDirection.MIN
        ):
            return 1
        else:
            return (
                (gb - pga - ga) / (vga - pga)
                if preference_direction == PreferenceDirection.MAX
                else (-gb - pga + ga) / (vga - pga)
            )

    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> DataFrame:
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix
        """
        return DataFrame(
            [
                [
                    Series(
                        {
                            j: self._discordance_index(
                                performance_table.df.loc[k, j],
                                performance_table.df.loc[i, j],
                                self.preference_thresholds[j],
                                self.veto_thresholds[j],
                                cast(
                                    QuantitativeScale,
                                    performance_table.scales[j],
                                ).preference_direction,
                            )
                            for j in performance_table.criteria
                        }
                    )
                    for i in performance_table.alternatives
                ]
                for k in performance_table.alternatives
            ],
            index=performance_table.alternatives,
            columns=performance_table.alternatives,
        )

    @staticmethod
    def _pairwise_credibility_index(
        pairwise_concordance_: float,
        pairwise_discordance_: Series,
    ) -> float:
        """Compute the credibility index between two alternatives.

        :pairwise_concordance_:
            concordance value for criterion between both alternatives
        :pairwise_discordance_:
            discordance serie for criterion between both alternatives
        :return: pairwise credibility index
        """
        sup_discordance = pairwise_discordance_[
            pairwise_discordance_ > pairwise_concordance_
        ]
        S_ab = pairwise_concordance_
        if len(sup_discordance) > 0:
            for Di_ab in sup_discordance:
                S_ab = S_ab * (1 - Di_ab) / (1 - pairwise_concordance_)
        return S_ab

    def construct(self, performance_table: PerformanceTable) -> DataFrame:
        """Compute the credibility matrix.

        :param performance_table:
        :return: credibility matrix
        """
        concordance_matrix = self.concordance(
            performance_table,
        )
        discordance_matrix = self.discordance(
            performance_table,
        )
        return DataFrame(
            [
                [
                    self._pairwise_credibility_index(
                        concordance_matrix.loc[i, j],
                        discordance_matrix.loc[i, j],
                    )
                    for j in performance_table.alternatives
                ]
                for i in performance_table.alternatives
            ],
            index=performance_table.alternatives,
            columns=performance_table.alternatives,
        )

    def qualification(self, credibility_mat: DataFrame) -> Series:
        """Compute the qualification for each pair of alternatives a and b.

        :param credibility_mat:
        :return: qualifications
        """
        lambda_max = max(credibility_mat.apply(max))
        lambda_ = lambda_max - (self.alpha + self.beta * lambda_max)

        lambda_strengths = Series(
            {
                i: sum(
                    (
                        credibility_mat.loc[i, j] > lambda_
                        and credibility_mat.loc[i, j]
                        > credibility_mat.loc[j, i]
                    )
                    for j in credibility_mat.index.tolist()
                )
                for i in credibility_mat.index.tolist()
            }
        )

        lambda_weakness = Series(
            {
                j: sum(
                    (
                        credibility_mat.loc[i, j] > lambda_
                        and credibility_mat.loc[i, j]
                        > credibility_mat.loc[j, i]
                    )
                    for i in credibility_mat.index.tolist()
                )
                for j in credibility_mat.index.tolist()
            }
        )

        return lambda_strengths - lambda_weakness

    def distillation(
        self,
        credibility_matrix: DataFrame,
        ascending: bool = False,
    ) -> List[List[Any]]:
        """Compute distillation.

        :param credibility_matrix:
        :param ascending: if ``True`` distillation is performed in ascension
        :return: ranking of categories
        """
        comp = min if ascending else max

        rest = credibility_matrix.index.tolist()
        distillate = []
        while len(rest) > 0:
            updated_credibility_mat = credibility_matrix.loc[rest]
            qualifications = self.qualification(
                updated_credibility_mat,
            )

            maxes = qualifications[qualifications == comp(qualifications)]
            if len(maxes) > 1:
                updated_credibility_mat = updated_credibility_mat.loc[
                    maxes.index
                ]
                qualifications = self.qualification(
                    updated_credibility_mat,
                )
                maxes = qualifications[qualifications == comp(qualifications)]
            distillate.append(maxes.index.tolist())
            for i in maxes.index.tolist():
                rest.remove(i)
        return distillate[::-1] if ascending else distillate

    def exploit(self, credibility_matrix: DataFrame) -> OutrankingMatrix:
        """Compute the complete Electre III exploitation phase.

        :param credibility_matrix:
        :return: final outranking matrix
        """
        return OutrankingMatrix.from_ranked_categories(
            self.distillation(credibility_matrix, ascending=True)
        ) * OutrankingMatrix.from_ranked_categories(
            self.distillation(credibility_matrix, ascending=False)
        )

    def __call__(
        self, performance_table: PerformanceTable, **kwargs
    ) -> OutrankingMatrix:
        """Compute the complete Electre III algorithm

        :param performance_table:
        :return: final outranking matrix
        """
        return self.exploit(self.construct(performance_table))


class ElectreTri(Electre):
    """This class implements the Electre-Tri B algorithm.

    :param criteria_weights:
    :param category_profiles:
    :param preference_thresholds:
    :param indifference_thresholds:
    :param veto_thresholds:
    :param lambda_: cut level

    .. note::
        Implementation and naming conventions are taken from
        :cite:p:`vincke1998electreTRI`.
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        category_profiles: PerformanceTable,
        preference_thresholds: Dict[Any, float],
        indifference_thresholds: Dict[Any, float],
        veto_thresholds: Dict[Any, float],
        lambda_: float,
    ):
        Electre.__init__(self, criteria_weights)
        self.category_profiles = category_profiles
        self.preference_thresholds = preference_thresholds
        self.indifference_thresholds = indifference_thresholds
        self.veto_thresholds = veto_thresholds
        self.lambda_ = lambda_

    @property
    def _electre3(self) -> Electre3:
        """Return the equivalent Electre3 object.

        :return:
        """
        return Electre3(
            self.criteria_weights,
            self.preference_thresholds,
            self.indifference_thresholds,
            self.veto_thresholds,
        )

    def concordance(
        self,
        performance_table: PerformanceTable,
    ) -> DataFrame:
        """Compute the concordance matrix.

        :param performance_table:
        :return: concordance matrix

        .. note:: uses :meth:`Electre3.concordance` implementation
        """
        return self._electre3.concordance(performance_table)

    def discordance(
        self,
        performance_table: PerformanceTable,
    ) -> DataFrame:
        """Compute the discordance matrix.

        :param performance_table:
        :return: discordance matrix

        .. note:: uses :meth:`Electre3.discordance` implementation
        """
        return self._electre3.discordance(performance_table)

    def construct(self, performance_table: PerformanceTable) -> DataFrame:
        """Return credibility matrix.

        Returned credibility matrix concatenates `performance_table`
        and :attr:`category_profiles` (in that order) and replaces labels with
        indexes to avoid duplicated indexes.

        :param performance_table:
        :return:

        .. note::
            uses :meth:`Electre3.construct` implementation
        """
        # Concatenate performance table and category profile
        # Replace indexes so no chance of same id category profile alternative
        altered_performance_table = PerformanceTable(
            performance_table.df.values.tolist()
            + self.category_profiles.df[
                performance_table.criteria
            ].values.tolist(),
            criteria=performance_table.criteria,
        )
        return DataFrame(
            self._electre3.construct(altered_performance_table),
        )

    def _pairwise_outrank(
        self,
        credibility_mat: DataFrame,
        alternative1: int,
        alternative2: int,
    ) -> Relation:
        """Compute relation between two actions based on credibility matrix.

        :param credibility_mat:
            credibility matrix of concatenated performance table / category
            profiles
        :param alternative1:
        :param alternative2:
        :return: relationship between both alternatives
        """
        aSb = cast(float, credibility_mat.loc[alternative1, alternative2])
        bSa = cast(float, credibility_mat.loc[alternative2, alternative1])
        if aSb >= self.lambda_ and bSa >= self.lambda_:
            return IndifferenceRelation(alternative1, alternative2)
        elif aSb >= self.lambda_ > bSa:
            return PreferenceRelation(alternative1, alternative2)
        elif aSb < self.lambda_ <= bSa:
            return PreferenceRelation(alternative2, alternative1)
        return IncomparableRelation(alternative1, alternative2)

    def _exploit(
        self,
        credibility_matrix: DataFrame,
        performance_table: PerformanceTable,
        pessimistic: bool = False,
    ) -> Dict[int, List[Any]]:
        """Compute the exploitation procedure (either optimistically or
        pessimistically).

        In the output ranking, class -1 means incomparable class

        :param credibility_matrix:
        :param performance_table:
        :param pessimistic: if ``True`` performs procedure pessimistically
        :return: categories
        """

        # performance table and category profiles are concatenated
        nb_classes = len(self.category_profiles.alternatives)
        nb_actions = len(credibility_matrix.index.tolist()) - nb_classes

        classes = defaultdict(list)
        rest = [*range(nb_actions)]
        for i in (
            range(nb_classes - 1, -1, -1) if pessimistic else range(nb_classes)
        ):
            class_ = []
            for action in rest:
                relation = self._pairwise_outrank(
                    credibility_matrix,
                    action,
                    i + nb_actions,
                )
                if isinstance(relation, PreferenceRelation):
                    if relation.a == action and pessimistic:
                        class_.append(action)
                        classes[i + 1].append(
                            performance_table.alternatives[action]
                        )
                    elif relation.b == action and not pessimistic:
                        class_.append(action)
                        classes[i].append(
                            performance_table.alternatives[action]
                        )
            for a in class_:
                rest.remove(a)
        if len(rest) > 0:
            for action in rest:
                relation = self._pairwise_outrank(
                    credibility_matrix,
                    nb_actions if pessimistic else action,
                    action if pessimistic else nb_actions + nb_classes - 1,
                )
                if isinstance(relation, IncomparableRelation):
                    classes[-1].append(performance_table.alternatives[action])
                elif relation.b == action and pessimistic:
                    classes[0].append(performance_table.alternatives[action])
                elif relation.a == action and not pessimistic:
                    classes[nb_classes].append(
                        performance_table.alternatives[action]
                    )
                else:
                    classes[-1].append(
                        performance_table.alternatives[action]
                    )  # pragma: nocover
        return classes

    def exploit(
        self,
        credibility_matrix: DataFrame,
        performance_table: PerformanceTable,
    ) -> Tuple[Dict[int, List[Any]], Dict[int, List[Any]]]:
        """Compute the exploitation procedure of Electre Tri.

        In the output ranking, class -1 means incomparable class

        :param credibility_matrix:
        :param performance_table:
        :return: optimistic categories, pessimistic categories
        """
        return self._exploit(
            credibility_matrix, performance_table
        ), self._exploit(
            credibility_matrix, performance_table, pessimistic=True
        )

    def __call__(
        self, performance_table: PerformanceTable, **kwargs
    ) -> Tuple[Dict[int, List[Any]], Dict[int, List[Any]]]:
        """Compute the exploitation procedure (either optimistically or
        pessimistically).

        In the output ranking, class -1 means incomparable class

        :param performance_table:
        :return: optimistic categories, pessimistic categories
        """
        return self.exploit(
            self.construct(performance_table=performance_table),
            performance_table,
        )
