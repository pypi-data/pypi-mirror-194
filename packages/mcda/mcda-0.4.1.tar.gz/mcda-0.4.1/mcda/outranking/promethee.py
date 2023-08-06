from abc import ABC, abstractmethod
from math import exp
from typing import Any, Dict, List, cast

import matplotlib.pyplot as plt
from pandas import DataFrame, Series
from sklearn.decomposition import PCA

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    PreferenceRelation,
    PreferenceStructure,
    Relation,
)

from ..core.scales import PreferenceDirection, QuantitativeScale


class PreferenceFunction(ABC):
    """This class define an interface for preference functions to share."""

    @abstractmethod
    def _apply_on_positive(self, x: float) -> float:  # pragma: nocover
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        pass

    def __call__(self, x: float) -> float:
        """Return preference degree on a criterion of two alternatives.

        :param x: criteria values difference
        :return:
        """
        if x <= 0:
            return 0
        return self._apply_on_positive(x)


class UShapeFunction(PreferenceFunction):
    """This class implements the u-shape preference function.

    :param q: the indifference threshold
    """

    def __init__(self, q: float):
        self.q = q

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.q else 0


class UsualFunction(UShapeFunction):
    """This class implements the usual preference function.

    This is actually a :class:`UShapeFunction` with 0 as the threshold.
    """

    def __init__(self):
        super().__init__(0)


class VShapeFunction(PreferenceFunction):
    """This class implements the v-shape preference function.

    :param p: preference threshold
    """

    def __init__(self, p: float):
        self.p = p

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.p else abs(x) / self.p


class LevelFunction(PreferenceFunction):
    """This class implements the level preference function.

    :param p: preference threshold
    :param q: indifference threshold
    """

    def __init__(self, p: float, q: float):
        if q > p:
            raise ValueError(f"incorrect threshold : q={q} greater than p={p}")
        self.p = p
        self.q = q

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return 1 if x > self.p else 0.5 if x > self.q else 0


class LinearFunction(LevelFunction):
    """This class implements the linear level preference function.

    :param p: preference threshold
    :param q: indifference threshold
    """

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of a positive criterion
        values difference.

        :param x: criteria values difference
        :return:
        """
        return (
            1
            if x > self.p
            else (abs(x) - self.q) / (self.p - self.q)
            if x > self.q
            else 0
        )


class GaussianFunction(PreferenceFunction):
    """This class implements the gaussian preference function.

    :param s: standard deviation
    """

    def __init__(self, s: float):
        self.s = s

    def _apply_on_positive(self, x: float) -> float:
        """Return preference degree on a criterion of two alternatives.

        :param x: criteria values difference
        :return:
        """
        return 1 - exp(-(x**2) / (2 * self.s**2))


class Promethee(ABC):
    """This class implements a common class for Promethee algorithms.

    :param criteria_weights:
    :param preference_functions: one function per criterion
    """

    def __init__(
        self,
        criteria_weights: Dict[Any, float],
        preference_functions: Dict[Any, PreferenceFunction],
    ):
        self.criteria_weights = criteria_weights
        self.preference_functions = preference_functions

    def pairwise_multicriteria_preference_degree(
        self,
        alternative_values1: ScaleValues,
        alternative_values2: ScaleValues,
    ) -> float:
        """Return the multicriteria preference degree of two alternatives.

        :param alternative_values1: criteria values for one alternative
        :param alternative_values2: criteria values for the second alternative
        :return:
        """
        weights = Series(self.criteria_weights)
        diffs = alternative_values1.data - alternative_values2.data
        pref_values = Series(
            {c: self.preference_functions[c](v) for c, v in diffs.items()}
        )
        return (weights * pref_values).sum() / weights.sum()

    @staticmethod
    def adapt_performance_table(performance_table: PerformanceTable):
        """Rearrange the performance table if there are criteria to minimize

        :param performance_table:
        :return: the scaled performance table
        """

        return performance_table.transform(
            {
                i: QuantitativeScale(
                    cast(QuantitativeScale, v).dmin,
                    cast(QuantitativeScale, v).dmax,
                    PreferenceDirection.MAX,
                )
                for i, v in performance_table.scales.items()
            },
        )

    def multicriteria_preference_degree(
        self, performance_table: PerformanceTable
    ) -> DataFrame:
        """Compute pairwise multicriteria preference degree for each
        alternatives' pair.

        Result can be summed along both axis to get the aggregated flows.
            * along axis ``0`` for the negative flow
            * along axis ``1`` for the positive flow

        :param performance_table:
        :return: matrix of pairwise multicriteria preference degrees
        """
        return DataFrame(
            [
                [
                    0
                    if ai == aj
                    else self.pairwise_multicriteria_preference_degree(
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

    @staticmethod
    def outranking_flows(matrix: DataFrame, negative: bool = False) -> Series:
        """Compute flow by aggregating multicriteria preference degrees.

        :param matrix:
            multicriteria preference degrees matrix (obtained by calling
            :meth:`multicriteria_preference_degree`
        :param negative: if ``True``, compute negative flows
        :return: flows
        """
        return matrix.sum(axis=0 if negative else 1)

    @abstractmethod
    def __call__(
        self, performance_table: PerformanceTable
    ) -> Any:  # pragma: nocover
        """Compute Promethee chosen algorithm and return result.

        :param performance_table:
        :return: result
        """
        pass


class Promethee1(Promethee):
    """This class implements Promethee I.

    Implementation and notations are based on :cite:p:`vincke1998promethee1`.

    :param criteria_weights:
    :param preference_functions: one function per criterion
    """

    @staticmethod
    def _flow_intersection(
        a: Any,
        b: Any,
        pos_flow_a: float,
        pos_flow_b: float,
        neg_flow_a: float,
        neg_flow_b: float,
    ) -> Relation:
        """Compute the positive and negative flow intersection.

        :param a: first alternative
        :param b: second alternative
        :param pos_flow_a: the positive flow of first alternative
        :param pos_flow_b: the positive flow of second alternative
        :param neg_flow_a: the negative flow of first alternative
        :param neg_flow_b: the negative flow of second alternative
        :return: the comparison of the two alternatives in a relation
        """

        if pos_flow_a == pos_flow_b and neg_flow_a == neg_flow_b:
            return IndifferenceRelation(a, b)
        if pos_flow_a >= pos_flow_b and neg_flow_a <= neg_flow_b:
            return PreferenceRelation(a, b)
        if pos_flow_b >= pos_flow_a and neg_flow_b <= neg_flow_a:
            return PreferenceRelation(b, a)
        return IncomparableRelation(a, b)

    def __call__(
        self, performance_table: PerformanceTable
    ) -> PreferenceStructure:
        """Apply Promethee I algorithm.

        :param performance_table:
        :return: result as a preference structure
        """
        table = self.adapt_performance_table(performance_table)
        degrees = self.multicriteria_preference_degree(table)
        pos_flow = self.outranking_flows(degrees)
        neg_flow = self.outranking_flows(degrees, negative=True)

        res = PreferenceStructure()
        for i, a in enumerate(table.alternatives):
            for b in table.alternatives[(i + 1) :]:
                res += self._flow_intersection(
                    a, b, pos_flow[a], pos_flow[b], neg_flow[a], neg_flow[b]
                )
        return res


class Promethee2(Promethee):
    """This class implements Promethee II.

    Implementation and notations are based on :cite:p:`vincke1998promethee1`.

    :param criteria_weights:
    :param preference_functions: one function per criterion
    """

    def __call__(self, performance_table: PerformanceTable) -> ScaleValues:
        """Apply Promethee I algorithm.

        :param performance_table:
        :return: result as scores
        """
        table = self.adapt_performance_table(performance_table)
        degrees = self.multicriteria_preference_degree(table)
        pos_flow = self.outranking_flows(degrees)
        neg_flow = self.outranking_flows(degrees, negative=True)

        return ScaleValues(pos_flow - neg_flow)


class PrometheeGaia(Promethee2):
    """This class is used to represent and draw a Promethee GAIA plane.

    Implementations naming conventions are taken from
    :cite:p:`figueira2005mcda`

    :param criteria_weights:
    :param preference_functions: one function per criterion
    """

    def unicriterion_net_flows_matrix(
        self, performance_table: PerformanceTable
    ) -> DataFrame:
        """Computes the whole matrix of single criterion net flows.

        Each cell corresponds to the single criterion net flow of an
        alternative considering only one criterion.

        :param performance_table:
        :return: unicriterion net flows matrix
        """
        df = DataFrame(
            0,
            index=performance_table.alternatives,
            columns=performance_table.criteria,
        )
        for a in performance_table.alternatives:
            for c in performance_table.criteria:
                df.loc[a, c] = Series(
                    {
                        other: self.preference_functions[c](
                            performance_table.df.loc[a, c]
                            - performance_table.df.loc[other, c]
                        )
                        - self.preference_functions[c](
                            performance_table.df.loc[other, c]
                            - performance_table.df.loc[a, c]
                        )
                        for other in performance_table.alternatives
                    }
                ).sum()
        return df

    def plot(self, performance_table: PerformanceTable):  # pragma: nocover
        """Plots the GAIA plane and displays in the top-left corner
        the ratio of saved information by the PCA, delta.

        :param performance_table:
        """
        net_flows = self.unicriterion_net_flows_matrix(performance_table)

        pca = PCA(n_components=2)
        pca.fit(net_flows)
        delta = (
            pca.explained_variance_ratio_[0] + pca.explained_variance_ratio_[1]
        )
        alternative_vectors = pca.transform(net_flows)
        criterions = DataFrame(
            [
                [
                    1 if i == j else 0
                    for j in range(len(performance_table.criteria))
                ]
                for i in range(len(performance_table.criteria))
            ],
            index=performance_table.criteria,
            columns=performance_table.criteria,
        )
        criterion_vectors = pca.transform(criterions)
        S = sum(self.criteria_weights.values())
        pi: List[float] = [0, 0]
        for criterion, w in self.criteria_weights.items():
            pi[0] += criterion_vectors[criterion][0] * w
            pi[1] += criterion_vectors[criterion][1] * w
        pi[0] = pi[0] / S
        pi[1] = pi[1] / S

        plt.figure(figsize=[10, 10])

        for i, alternative in enumerate(performance_table.alternatives):
            plt.scatter(
                alternative_vectors[i][0],
                alternative_vectors[i][1],
                s=100,
                label=alternative,
            )
        for j, criterion in enumerate(performance_table.criteria):
            plt.text(
                criterion_vectors[j][0],
                criterion_vectors[j][1],
                criterion,
                ha="center",
            )
            plt.arrow(
                0,
                0,
                criterion_vectors[j][0],
                criterion_vectors[j][1],
            )

        plt.arrow(0, 0, pi[0], pi[1])
        plt.scatter(pi[0], pi[1], s=150, marker="*", label=r"$\pi$")

        ax = plt.gca()
        xmin, _ = ax.get_xlim()
        _, ymax = ax.get_ylim()

        plt.text(
            xmin, ymax, r"$\delta$ = %.3f" % delta, bbox=dict(boxstyle="round")
        )

        plt.legend()
        plt.plot()
        plt.show()
