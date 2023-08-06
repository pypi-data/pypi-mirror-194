from __future__ import annotations

from typing import Any, Dict, Iterator, List, Union, cast

from pandas import DataFrame, Series
from pandas.api.types import is_numeric_dtype  # type: ignore

from mcda.core.aliases import Function
from mcda.core.matrices import Matrix
from mcda.core.scales import (
    NominalScale,
    PreferenceDirection,
    QuantitativeScale,
    Scale,
)


def series_equals(s1: Series, s2: Series) -> bool:
    """Check if two series have the same values.

    It will realign the indexes if they are ordered differently.

    :param s1:
    :param s2:
    :return:
    """
    return dict(s1) == dict(s2)


class Values:
    """This class is a wrapper around :class:`pandas.Series`.

    It is intended to be used for all classes across the package that uses
    a Series as their internal data representation.

    :param data: series containing the data

    :attr data: internal representation of data
    """

    def __init__(self, data: Series):
        self.data = Series(data)

    def __eq__(self, other: Any) -> bool:
        """Check if both values have the same data

        :return:

        .. note:: values order does not matter
        """
        if type(other) != type(self):
            return False
        return series_equals(self.data, other.data)

    @property
    def name(self) -> Any:
        """Return the name of the :attr:`data` attribute."""
        return self.data.name

    @property
    def labels(self) -> List[Any]:
        """Return the data labels."""
        return self.data.index.tolist()

    @property
    def is_numeric(self) -> bool:
        """Check whether values are numeric.

        :return:
        :rtype: bool
        """
        return is_numeric_dtype(self.data)

    def sum(self) -> float:
        """Return the sum of the data.

        :return:

        .. warning::
            it will raise a :class:`TypeError` if data contains numeric
            and non-numeric values
        """
        return sum(self.data)

    def copy(self) -> "Values":
        """Return a copy of the object"""
        return Values(self.data.copy())

    def __iter__(self) -> Iterator:
        """Return an iterator over the data."""
        return iter(self.data)

    def __getitem__(self, item: Any) -> Any:
        """Return the value of the data at a specific label.

        :return:
        """
        return self.data[item]

    def __setitem__(self, key: Any, value: Any):
        """Set the value of the data at a specific label."""
        self.data[key] = value


class ScaleValues(Values):
    """This class associates a data :class:`pandas.Series` with their
    multiple :class:`mcda.core.Scale`.

    :param data: series containing the data
    :param scales:
        data scale(s) (one per value or one shared, will be inferred from data
        if absent using :meth:`ScaleValues.bounds`)
    :param preference_direction: (ignored is `scales` supplied)
    :raise KeyError: if `scales` keys and `data` indexes mismatch

    :attr data: internal representation of data
    :attr scales: scales of the data (one per value)
    """

    def __init__(
        self,
        data: Series,
        scales: Scale | Dict[Any, Scale] | None = None,
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        super().__init__(data)
        scales = (
            self._bounds(preference_direction) if scales is None else scales
        )
        if isinstance(scales, Scale):
            scales = {k: scales for k in self.labels}
        self.scales = scales
        if set(self.labels) != set(self.scales.keys()):
            raise KeyError("data and scales must have the same labels")

    def _bounds(
        self,
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ) -> Scale:
        """Infer one common scale from the data.

        It returns a :class:`mcda.core.scales.QuantitativeScale` for numeric
        data, a :class:`mcda.core.scales.NominalScale` otherwise.

        :param preference_direction:
        :return: inferred scale
        """
        if self.is_numeric:
            return QuantitativeScale(
                self.data.min(), self.data.max(), preference_direction
            )
        return NominalScale(cast(List[Any], list(set(self.data.values))))

    def __eq__(self, other: Any) -> bool:
        """Check equality of scale values.

        Equality is defines as having the same set of scales, and having the
        same data.

        :return: ``True`` if both are equal
        """
        if not isinstance(other, ScaleValues):
            return False
        _values = cast(ScaleValues, other)
        if self.scales == _values.scales:
            return super().__eq__(_values)
        return False

    @property
    def bounds(self) -> Scale:
        """Infer one common scale from the data.

        It returns a :class:`mcda.core.scales.QuantitativeScale` with maximize
        preference direction for numeric data, a
        :class:`mcda.core.scales.NominalScale` otherwise.

        :return: inferred scale
        """
        return self._bounds()

    @property
    def within_scales(self) -> "ScaleValues":
        """Return a series indicating which values are within their
        respective scale.

        :return:
        """

        return self.__class__(
            Series({k: v in self.scales[k] for k, v in self.data.items()}),
            self.scales,
        )

    @property
    def is_within_scales(self) -> bool:
        """Check whether all values are within their respective scales.

        :return:
        """
        return self.within_scales.data.all()

    def transform_to(
        self, out_scales: Dict[Any, Scale] | Scale
    ) -> "ScaleValues":
        """Return data transformed to the target scales.

        :return:
        """
        out_scales = (
            {k: out_scales for k in self.labels}
            if isinstance(out_scales, Scale)
            else out_scales
        )
        return ScaleValues(
            Series(
                {
                    k: self.scales[k].transform_to(v, out_scales[k])
                    for k, v in self.data.items()
                }
            ),
            out_scales,
        )

    def normalize(self) -> "ScaleValues":
        """Return normalized data.

        :return:
        """
        return self.transform_to(QuantitativeScale.normal())

    def sort(self, reverse: bool = False) -> "ScaleValues":
        """Return sorted data in new instance.

        Normalized data are used to determine the sorting order.

        :param reverse: if ``True``, will sort in ascending order
        :return:
        """
        normalized = self.normalize()
        copy = self.copy()
        copy.data = self.data[
            normalized.data.sort_values(ascending=reverse).index
        ]
        return copy

    def copy(self) -> "ScaleValues":
        """Return a copy of the object"""
        return ScaleValues(self.data.copy(), self.scales.copy())


class Scores(ScaleValues):
    """This class describes a scores as a :class:`ScaleValues`.

    It is intended as a shorthand to create scores.

    :param data:
    :param preference_direction:
    :raise ValueError: if `data` contains non-numeric values

    :attr data: internal representation of data
    :attr scales:
        scales of the data (one per value, all equals to the same
        :class:`mcda.core.scales.QuantitativeScale` with bounds inferred from
        data)
    """

    def __init__(
        self,
        data: Series,
        preference_direction: PreferenceDirection = PreferenceDirection.MAX,
    ):
        self.preference_direction = preference_direction
        if not is_numeric_dtype(data):
            raise ValueError(f"{self.__class__} only supports numeric values")
        super().__init__(data=data, preference_direction=preference_direction)

    def copy(self) -> "Scores":
        """Return a copy of the object"""
        return Scores(self.data.copy(), self.preference_direction)


class PerformanceTable(Matrix):
    """This class is used to represent performance tables.

    :param data: performance table in an array-like or dict structure
    :param scales: criteria scales (scales are inferred from data if not set)
    :param alternatives:
    :param criteria:

    :attr df: dataframe containing the performances
    :attr scales: criteria scales

    .. note::
        when applying pandas methods to modify the performance table, do it
        this way: `table.df = table.df.method()` (for a method called `method`)

        Also you may want to modify the criteria scales depending on such
        modifications.
    """

    def __init__(
        self,
        data,
        scales: Dict[Any, Scale] = None,
        alternatives: List[Any] = None,
        criteria: List[Any] = None,
    ):
        df = DataFrame(data, index=alternatives, columns=criteria)
        super().__init__(df)
        self.scales = self.bounds if scales is None else scales

    def __eq__(self, other) -> bool:
        """Check equality of performance tables.

        Equality is defines as having the same set of scales, and having the
        same dataframe.

        :return: ``True`` if both are equal
        """
        if not isinstance(other, PerformanceTable):
            return False
        _table = cast(PerformanceTable, other)
        if self.scales == _table.scales:
            return super().__eq__(_table)
        return False

    @property
    def criteria(self) -> List[Any]:
        """Return performance table criteria"""
        return self.df.columns.tolist()

    @property
    def alternatives(self) -> List[Any]:
        """Return performance table alternatives"""
        return self.df.index.tolist()

    @property
    def alternatives_values(self) -> Iterator[ScaleValues]:
        """Iterator on the table alternatives values"""
        for alternative in self.alternatives:
            yield self.get_alternative_values(alternative)

    @property
    def criteria_values(self) -> Iterator[ScaleValues]:
        """Iterator on the table criteria values"""
        for criterion in self.criteria:
            yield self.get_criterion_values(criterion)

    @property
    def is_numeric(self) -> bool:
        """Check whether performance table is numeric.

        :return:
        :rtype: bool
        """
        for col in self.df.columns:
            if not is_numeric_dtype(self.df[col]):
                return False
        return True

    @property
    def bounds(self) -> Dict[Any, Scale]:
        """Return criteria scales inferred from performance table values.

        .. note::
            will always assume maximizable quantitative scales for numeric
            criteria and nominal scales for others
        """
        return {
            criterion: ScaleValues(self.df[criterion]).bounds
            for criterion in self.criteria
        }

    def get_alternative_values(self, alternative: Any) -> ScaleValues:
        """Get performances associated to an alternative.

        :param alternative: alternative label
        :return:
        """
        return ScaleValues(self.df.loc[alternative], self.scales)

    def get_criterion_values(self, criterion: Any) -> ScaleValues:
        """Get performances associated to a criterion.

        :param criterion: criterion label
        :return:
        """
        return ScaleValues(self.df[criterion], self.scales[criterion])

    def get_alternative_values_at(self, index: int) -> ScaleValues:
        """Get performances associated to an alternative index.

        :param index: alternative index
        :return:
        """
        return ScaleValues(self.df.iloc[index], self.scales)

    def get_criterion_values_at(self, index: int) -> ScaleValues:
        """Get performances associated to a criterion index.

        :param index: criterion index
        :return:
        """
        return ScaleValues(
            self.df.iloc[:, index], self.scales[self.criteria[index]]
        )

    def apply_criteria_functions(
        self, functions: Dict[Any, Function]
    ) -> "PerformanceTable":
        """Apply criteria functions to performance table and return result.

        :param functions: functions identified by their criterion
        :return:
        """
        return PerformanceTable(
            self.df.apply(
                lambda col: col.apply(functions.get(col.name, lambda x: x))
            ),
            self.scales,
        )

    def apply_criteria_weights(
        self,
        criteria_weights: Dict[Any, float],
    ) -> "PerformanceTable":
        """Apply criteria weights to a performance table and return result.

        :param criteria_weights: weights identified by their criterion
        :return:
        """
        return self.apply_criteria_functions(
            {
                criterion: (
                    cast(
                        Function,
                        lambda x, w=criterion_weight: w * cast(float, x),
                    )
                )
                for criterion, criterion_weight in criteria_weights.items()
            },
        )

    @property
    def within_criteria_scales(self) -> "PerformanceTable":
        """Return a table indicating which performances are within their
        respective criterion scale.

        :return:
        """
        return self.apply_criteria_functions(
            {
                criterion: cast(
                    Function, lambda x, c=criterion: x in self.scales[c]
                )
                for criterion in self.scales.keys()
            },
        )

    @property
    def is_within_criteria_scales(self) -> bool:
        """Check whether all cells are within their respective criteria scales.

        :return:
        """
        return self.within_criteria_scales.df.all(None)

    def transform(
        self,
        out_scales: Dict[Any, Scale],
    ) -> "PerformanceTable":
        """Transform performances table between scales.

        :param out_scales: target criteria scales
        :return: transformed performance table
        """
        functions = {
            criterion: (
                cast(
                    Function,
                    lambda x, c=criterion: self.scales[c].transform_to(
                        x, out_scales[c]
                    ),
                )
            )  # https://bugs.python.org/issue13652
            for criterion in self.scales.keys()
        }
        return PerformanceTable(
            self.apply_criteria_functions(functions).df, out_scales
        )

    def normalize_without_scales(self) -> "PerformanceTable":
        """Normalize performance table using criteria values bounds.

        :return:
        :raise TypeError: if performance table is not numeric
        """
        return PerformanceTable(self.df).normalize()

    def normalize(self) -> "PerformanceTable":
        """Normalize performance table using criteria scales.

        :return:
        """
        return self.transform(
            {
                criterion: QuantitativeScale.normal()
                for criterion in self.criteria
            }
        )

    def sum(self, axis: int = None) -> Union[Series, float]:
        """Sum performances.

        Behaviour depends on `axis` value:

        * ``0``: returns column sums as a list
        * ``1``: returns row sums as a list
        * else: returns sum on both dimension as a numeric value

        :param axis: axis on which the sum is made
        :return:

        .. note::
            Non-numeric values are simply ignored as well as non-numeric sums
        """
        if axis is not None:
            return self.df.sum(axis=axis, numeric_only=True)
        return self.df.sum(numeric_only=True).sum()

    def subtable(
        self, alternatives: List[Any] = None, criteria: List[Any] = None
    ) -> "PerformanceTable":
        """Return the subtable containing given alternatives and criteria.

        :param alternatives:
        :param criteria:
        :return:
        """
        alternatives = (
            self.alternatives if alternatives is None else alternatives
        )
        criteria = self.criteria if criteria is None else criteria
        return self.__class__(
            self.df.loc[alternatives, criteria],
            {criterion: self.scales[criterion] for criterion in criteria},
        )
