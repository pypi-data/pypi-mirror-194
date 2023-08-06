"""This module gathers aggregators
"""

from abc import ABC, abstractmethod
from math import log
from typing import Any, Dict, List, Union, cast

from pandas import DataFrame, Series

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.set_functions import Capacity, MobiusCapacity

from ..core.aliases import NumericFunction
from ..core.functions import FuzzyNumber
from ..core.scales import FuzzyScale, QuantitativeScale, Scale
from ..plot.plot import Figure, LinePlot


class Aggregator(ABC):
    """This abstract class represents a typical aggregator."""

    @abstractmethod
    def _apply_series(
        self, series: Series, *args, **kwargs
    ) -> Any:  # pragma: nocover
        """Apply aggregation method to a pandas Series.

        :param series:
        """
        pass

    def _apply_scale_values(
        self, scale_values: ScaleValues, *args, **kwargs
    ) -> Any:
        """Apply aggregation method to a scale values object.

        :param scale_values:
        """
        return self._apply_series(scale_values.data)

    def _apply_dataframe(self, df: DataFrame, *args, **kwargs) -> Series:
        """Apply aggregation method to a pandas DataFrame.

        :param df:
        :return: aggregated rows
        """
        return Series(
            {
                alternative: self._apply_series(
                    df.loc[alternative], *args, **kwargs
                )
                for alternative in df.index.tolist()
            }
        )

    def _apply_performance_table(
        self, performance_table: PerformanceTable, *args, **kwargs
    ) -> Series:
        """Apply aggregation method to a performance table object.

        :param performance_table:
        :return: aggregated criteria values per alternative
        """
        return self._apply_dataframe(performance_table.df, *args, **kwargs)

    def __call__(
        self, data: Union[PerformanceTable, DataFrame, Series], *args, **kwargs
    ) -> Any:
        """Apply aggregation method to input data.

        :param data:
        :return: aggregation result

        .. note:: aggregation is applied for each row in case of tabular data
        """
        if isinstance(data, PerformanceTable):
            return self._apply_performance_table(data, *args, **kwargs)
        if isinstance(data, DataFrame):
            return self._apply_dataframe(data, *args, **kwargs)
        if isinstance(data, ScaleValues):
            return self._apply_scale_values(data, *args, **kwargs)
        return self._apply_series(data, *args, **kwargs)


class WeightedSum(Aggregator):
    """This class represents a weighted sum aggregator.

    :param criteria_weights:
    """

    def __init__(self, criteria_weights: Union[Dict[Any, float], Series]):
        self.criteria_weights = Series(criteria_weights)

    def _apply_series(self, series: Series, *args, **kwargs) -> float:
        """Return weighted sum of the input.

        :param series:
        :return:
        """
        return (series * self.criteria_weights).sum()


class ChoquetIntegral(Aggregator):
    """This class represents a Choquet integral aggregator.

    :param capacity:
        capacity used for aggregation (either in regular or Möbius
        representation)

    .. note:: Implementation is based on :cite:p:`grabisch2008review`.
    """

    def __init__(self, capacity: Union[Capacity, MobiusCapacity]):
        self.capacity = capacity

    def _choquet_integral_capacity(self, series: Series) -> float:
        """Return Choquet integral using a capacity.

        :param series:
        :return:

        .. note:: Implementation is based on :cite:p:`grabisch2008review`.
        """
        res = series.sort_values()
        criteria = res.index.tolist()
        return sum(
            res[criterion]
            * (
                self.capacity(*criteria[i:])
                - self.capacity(*criteria[(i + 1) :])
            )
            for i, criterion in enumerate(criteria)
        )

    def _choquet_integral_mobius(self, series: Series) -> float:
        """Return Choquet integral using a möbius.

        :param series:
        :return:

        .. note:: Implementation is based on :cite:p:`grabisch2008review`.
        """
        return sum(
            m * series[list(t)].min()
            for t, m in self.capacity.values.items()
            if len(t) > 0
        )

    def _apply_series(self, series: Series, *args, **kwargs) -> float:
        """Return Choquet integral of the pandas Series.

        :param series:
        :return:
        """
        if isinstance(self.capacity, MobiusCapacity):
            return self._choquet_integral_mobius(series)
        return self._choquet_integral_capacity(series)


class OWA(Aggregator):
    """This class represents an Ordered Weighted Aggregator (OWA).

    :param weights:

    .. note:: Implementation is based on :cite:p:`grabisch2008review`.
    """

    def __init__(self, weights: List[float]):
        self.weights = weights

    @property
    def orness(self) -> float:
        """Return *orness* measure of OWA weights.

        :return:

        .. note:: *orness* as defined in :cite:p:`yager1988owa`
        """
        return sum(
            (len(self.weights) - i - 1) * w for i, w in enumerate(self.weights)
        ) / (len(self.weights) - 1)

    @property
    def andness(self) -> float:
        """Return *andness* measure of OWA weights.

        :return:

        .. note:: *andness* as defined in :cite:p:`yager1988owa`
        """
        return 1 - self.orness

    @property
    def dispersion(self) -> float:
        """Return OWA weights dispersion (also called entropy).

        :return:

        .. note:: dispersion as defined in :cite:p:`yager1988owa`
        """
        return -sum(w * log(w) if w > 0 else 0 for w in self.weights)

    @property
    def divergence(self) -> float:
        """Return OWA weights divergence.

        :return:

        .. note:: divergence as defined in :cite:p:`yager2002heavy`
        """
        addition = 0.0
        j = 1
        n = len(self.weights)
        orness = self.orness
        for w in self.weights:
            operation = (((n - j) / (n - 1)) - orness) ** 2
            j = j + 1
            addition = addition + w * operation
        return addition

    @property
    def balance(self) -> float:
        """Return OWA weights balance.

        :return:

        .. note:: balance as defined in :cite:p:`yager1996constrainedowa`
        """
        addition = 0.0
        j = 1
        n = len(self.weights)
        for w in self.weights:
            operation = (n + 1 - 2 * j) / (n - 1)
            j = j + 1
            addition = addition + w * operation
        return addition

    @property
    def quantifier(self) -> List[float]:
        """Return quantifier corresponding to OWA weights.

        :return:

        .. note:: quantifier as defined in :cite:p:`yager1988owa`
        """
        return [
            sum(w for w in self.weights[:i])
            for i in range(len(self.weights) + 1)
        ]

    def _apply_series(self, series: Series, *args, **kwargs) -> float:
        """Return Ordered Weighted Aggregation of values.

        :param series:
        :return:

        .. note:: Implementation is based on :cite:p:`yager1988owa`
        """
        return (series.sort_values(ascending=False) * self.weights).sum()

    @classmethod
    def from_quantifier(cls, quantifier: List[float]) -> "OWA":
        """Return OWA aggregator corresponding to given quantifier.

        :param quantifier:
        :return:

        .. note:: quantifier as defined in :cite:p:`yager1988owa`
        """
        return cls(
            [q - q_1 for q, q_1 in zip(quantifier[1:], quantifier[:-1])]
        )

    @classmethod
    def and_aggregator(cls, size: int) -> "OWA":
        """Return *and* OWA aggregator of given weights size.

        :param size:
        :return:

        .. note:: :math:`W_*` as defined in :cite:p:`yager1988owa`
        """
        return cls(cast(List[float], [0] * (size - 1) + [1]))

    @classmethod
    def or_aggregator(cls, size: int) -> "OWA":
        """Return *or* OWA aggregator of given weights size.

        :param size:
        :return:

        .. note:: :math:`W^*` as defined in :cite:p:`yager1988owa`
        """
        return cls(cast(List[float], [1] + [0] * (size - 1)))


class ULOWA(Aggregator):
    """This class represents an Unbalanced Linguistic Weighted Average (ULOWA)
    aggregator.

    :param weights:
    :param scale: fuzzy scale used for the average

    .. note:: implementation based on :cite:p:`isern2010ulowa`
    """

    def __init__(self, weights: List[float], scale: FuzzyScale):
        self.weights = weights
        self.scale = scale

    @staticmethod
    def delta(a: Any, b: Any, weight: float, scale: FuzzyScale) -> float:
        """Returns ULOWA delta value.

        :param a: worst value
        :param b: best value
        :param weight: ULOWA weight
        :param scale: fuzzy scale
        :return:
        """
        xa = cast(float, scale.transform_to(a))
        xb = cast(float, scale.transform_to(b))
        return xa + weight * (xb - xa)

    @staticmethod
    def most_similar(
        a: Any, b: Any, ref_fuzzy: FuzzyNumber, scale: FuzzyScale
    ) -> Any:
        """Returns label which fuzzy number is the most similar to the
        reference (between `a` and `b` labels).

        :param a:
        :param b:
        :param ref_fuzzy: fuzzy number that is being compared to
        :param scale: fuzzy scale
        :return:
        """
        if scale.ordinal_distance(a, b) == 1:
            _labels = [a, b]
        else:
            _labels = sorted(
                scale.labels, key=lambda v: scale.transform_to(v), reverse=True
            )
            lmin = min(_labels.index(a), _labels.index(b))
            lmax = max(_labels.index(a), _labels.index(b))
            _labels = _labels[lmin : lmax + 1]
        sims = [
            scale.similarity(scale.fuzzy[scale.labels.index(v)], ref_fuzzy)
            for v in _labels
        ]
        return _labels[max(range(len(_labels)), key=lambda i: sims[i])]

    def _apply_series(
        self, series: Series, *args, weights=None, **kwargs
    ) -> Any:
        """Returns Unbalanced Linguistic Weighted Average of values.

        :param values:
        :param weights:
        :return:
        :raise ValueError: if `values` contains less than 2 items

        .. note:: implementation based on :cite:p:`isern2010ulowa`

        .. warning::
            this function is intended for use with a fuzzy scale defining a
            fuzzy partition
        """
        values = sorted(
            series.tolist(),
            key=lambda v: self.scale.transform_to(v),
            reverse=True,
        )
        weights = self.weights.copy() if weights is None else weights
        if len(values) == 0:
            raise ValueError("ULOWA needs at least one value")
        if len(values) == 1:
            return values[0]
        denominator = weights[-2] + weights[-1]
        weight = 0 if denominator == 0 else weights[-2] / denominator
        delta = self.delta(values[-1], values[-2], weight, self.scale)
        values[-2] = self.most_similar(
            values[-1], values[-2], FuzzyNumber([delta] * 4), self.scale
        )
        weights[-2] += weights[-1]
        return self._apply_series(Series(values[:-1]), weights=weights[:-1])


class UtilityFunction(Aggregator):
    """This class represents a multi-attribute utility functions aggregator.

    :param criteria_functions:
    :param scales: normalized scales are used if not provided

    .. note::
        `criteria_functions` are defined for the provided scales, so when
        applying aggregation you must provide correctly scaled values (only
        :class:`mcda.api.core/performance_table.PerformanceTable`
        and :class:`mcda.api.core.performance_table.ScaleValues` are
        automatically transformed)
    """

    def __init__(
        self,
        criteria_functions: Dict[Any, NumericFunction],
        scales: Dict[Any, QuantitativeScale] = None,
    ):
        self.criteria_functions = criteria_functions
        self.scales = (
            scales
            if scales is not None
            else {
                c: QuantitativeScale.normal()
                for c in criteria_functions.keys()
            }
        )

    def _apply_series(self, series: Series, *args, **kwargs) -> float:
        """Apply aggregation method to a pandas Series.

        :param series:
        """
        res = Series(
            {
                criterion: self.criteria_functions[criterion](value)
                for criterion, value in dict(series).items()
            }
        )
        return res.sum()

    def _apply_scale_values(
        self, scale_values: ScaleValues, *args, **kwargs
    ) -> float:
        """Apply aggregation method to a scale values object.

        :param scale_values:
        :return: aggregated criteria values

        .. note::
            `scale_values` values are transformed to utility functions `scales`
        """
        return self._apply_series(
            scale_values.transform_to(cast(Dict[Any, Scale], self.scales)).data
        )

    def _apply_dataframe(self, df: DataFrame, *args, **kwargs) -> Series:
        """Apply aggregation method to a pandas DataFrame.

        :param df:
        :return: aggregated rows
        """
        res = cast(
            DataFrame,
            df.apply(
                lambda col: col.apply(self.criteria_functions.get(col.name))
            ),
        )
        return res.sum(axis=1)

    def _apply_performance_table(
        self, performance_table: PerformanceTable, *args, **kwargs
    ) -> Series:
        """Apply aggregation method to a performance table object.

        :param performance_table:
        :return: aggregated criteria values per alternative

        .. note::
            `performance_table` values are transformed to utility functions
            `scales`
        """
        return self._apply_dataframe(
            performance_table.transform(cast(Dict[str, Scale], self.scales)).df
        )

    def plot(self, nb_points=500) -> Figure:  # pragma: nocover
        """Plot each criterion function on its respective scale.

        :return: created figure
        """
        fig = Figure(ncols=2)
        for c, scale in self.scales.items():
            x = cast(List[float], scale.range(nb_points))
            y = [self.criteria_functions[c](xx) for xx in x]
            ax = fig.create_add_axis()
            ax.title = c
            ax.add_plot(LinePlot(x, y))
        fig.draw()
        return fig
