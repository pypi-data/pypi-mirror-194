import unittest

from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal, assert_series_equal

from mcda.core.functions import DiscreteFunction
from mcda.core.performance_table import (
    PerformanceTable,
    ScaleValues,
    Scores,
    Values,
    series_equals,
)
from mcda.core.scales import (
    NominalScale,
    PreferenceDirection,
    QualitativeScale,
    QuantitativeScale,
)


def test_series_equals():
    s1 = Series([0, 1, 2, 3])
    s2 = Series([3, 2, 1, 0], index=[3, 2, 1, 0])
    assert series_equals(s1, s2)
    assert not series_equals(s1, Series({"0": 0, 1: 1, 2: 2, 3: 3}))
    assert not series_equals(s1, Series([1, 1, 2, 3]))


class ValuesTestCase(unittest.TestCase):
    def setUp(self):
        self.data = Series([0, 1, 2, 3, 4], name="Test")
        self.values = Values(self.data)

    def test_constructor(self):
        assert_series_equal(self.data, self.values.data)
        self.assertEqual(self.values.name, self.data.name)
        self.assertEqual(self.values.labels, [*range(len(self.data))])
        self.assertTrue(self.values.is_numeric)

    def test_equal(self):
        self.assertNotEqual(self.values, self.data)
        self.assertNotEqual(self.values, Series([0, 1, 5, 3, 4], name="Test"))
        self.assertEqual(Values(self.data), self.values)

    def test_sum(self):
        self.assertEqual(self.values.sum(), 10)

    def test(self):
        self.assertEqual(self.values[0], self.data[0])
        values = Values(self.data)
        values[0] = 10
        self.assertEqual(values.data[0], 10)
        self.assertEqual([*iter(self.values)], self.data.values.tolist())

    def test_copy(self):
        copy = self.values.copy()
        assert_series_equal(copy.data, self.values.data)


class ScaleValuesTestCase(unittest.TestCase):
    def setUp(self):
        self.scales = {
            "c01": QualitativeScale(
                Series({"*": 1, "**": 2, "***": 3, "****": 4})
            ),
            "c02": QualitativeScale(
                Series({"Perfect": 1, "Good": 2, "Bad": 3}),
                PreferenceDirection.MIN,
            ),
            "c03": QuantitativeScale(0, 25000, PreferenceDirection.MIN),
        }
        self.data = Series(
            ["**", "Perfect", 12000], index=["c01", "c02", "c03"], name="a00"
        )
        self.values = ScaleValues(self.data, self.scales)

    def test_constructor(self):
        assert_series_equal(self.data, self.values.data)
        self.assertEqual(self.values.scales, self.scales)
        v1 = ScaleValues(Series([0, 1, 2]))
        self.assertEqual(
            v1.scales, {k: QuantitativeScale(0, 2) for k in range(3)}
        )
        v2 = ScaleValues(Series([0, -10, 5, 12]), QuantitativeScale(-20, 20))
        self.assertEqual(
            v2.scales, {k: QuantitativeScale(-20, 20) for k in range(4)}
        )
        v3 = ScaleValues(
            Series([0, 1, 2]), preference_direction=PreferenceDirection.MIN
        )
        self.assertEqual(
            v3.scales,
            {
                k: QuantitativeScale(0, 2, PreferenceDirection.MIN)
                for k in range(3)
            },
        )
        self.assertRaises(
            KeyError,
            ScaleValues,
            Series([0, 1]),
            {"a": QuantitativeScale.normal(), "b": QuantitativeScale.normal()},
        )

    def test_equal(self):
        self.assertNotEqual(self.values, self.data)
        self.assertNotEqual(
            self.values,
            ScaleValues(
                Series([0, 1, 2], index=["c01", "c02", "c03"], name="a00")
            ),
        )
        self.assertEqual(
            ScaleValues(self.data, self.scales),
            self.values,
        )

    def test_bounds(self):
        expected = NominalScale(["**", "Perfect", 12000])
        self.assertEqual(self.values.bounds, expected)
        v1 = ScaleValues(Series([0, 1, 2]))
        self.assertEqual(v1.bounds, QuantitativeScale(0, 2))

    def test_within_scales(self):
        self.assertTrue(self.values.within_scales.data.all(axis=None))

    def test_is_within_criteria_scales(self):
        self.assertTrue(self.values.is_within_scales)

    def test_transform(self):
        out_scales = {
            "c01": self.scales["c01"].quantitative,
            "c02": self.scales["c02"].quantitative,
            "c03": QuantitativeScale(0, 100),
        }
        expected = Series({"c01": 2, "c02": 1, "c03": 52})
        res = self.values.transform_to(out_scales)
        assert_series_equal(res.data, expected, check_dtype=False)
        self.assertEqual(res.scales, out_scales)

    def test_normalize(self):
        expected = Series({"c01": 1 / 3, "c02": 1, "c03": 0.52})
        res = self.values.normalize()
        assert_series_equal(expected, res.data)
        self.assertEqual(
            res.scales, {k: QuantitativeScale.normal() for k in res.labels}
        )

    def test_sort(self):
        expected = ["c02", "c03", "c01"]
        self.assertEqual(self.values.sort().labels, expected)

    def test_copy(self):
        copy = self.values.copy()
        assert_series_equal(copy.data, self.values.data)
        self.assertEqual(copy.scales, self.values.scales)


class ScoresTestCase(unittest.TestCase):
    def setUp(self):
        self.data = Series([0, 1, 2])
        self.scores = Scores(self.data)

    def test_constructor(self):
        self.assertEqual(
            self.scores.scales,
            {
                k: QuantitativeScale(0, 2, PreferenceDirection.MAX)
                for k in range(3)
            },
        )
        self.assertRaises(ValueError, Scores, Series([1, "haha"]))

    def test_copy(self):
        copy = self.scores.copy()
        assert_series_equal(copy.data, self.scores.data)
        self.assertEqual(copy.scales, self.scores.scales)
        self.assertEqual(
            copy.preference_direction, self.scores.preference_direction
        )


class PerformanceTableTestCase(unittest.TestCase):
    def setUp(self):
        self.alternatives = ["a01", "a02", "a03", "a04"]
        self.criteria = ["c01", "c02", "c03"]
        self.scales = {
            "c01": QualitativeScale(
                Series({"*": 1, "**": 2, "***": 3, "****": 4})
            ),
            "c02": QualitativeScale(
                Series({"Perfect": 1, "Good": 2, "Bad": 3}),
                PreferenceDirection.MIN,
            ),
            "c03": QuantitativeScale(0, 25000, PreferenceDirection.MIN),
        }
        self.numeric_scales = {
            "c01": QuantitativeScale(1, 4),
            "c02": QuantitativeScale(1, 3, PreferenceDirection.MIN),
            "c03": QuantitativeScale(0, 25000, PreferenceDirection.MIN),
        }
        self.df = DataFrame(
            [
                ["*", "Good", 5000],
                ["***", "Bad", 12000],
                ["**", "Perfect", 8500],
                ["****", "Good", 18635.2],
            ],
            index=self.alternatives,
            columns=self.criteria,
        )
        self.performance_table = PerformanceTable(
            [
                ["*", "Good", 5000],
                ["***", "Bad", 12000],
                ["**", "Perfect", 8500],
                ["****", "Good", 18635.2],
            ],
            scales=self.scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        self.numeric_table = PerformanceTable(
            [
                [1, 2, 5000],
                [3, 3, 12000],
                [2, 1, 8500],
                [4, 2, 18635.2],
            ],
            scales=self.numeric_scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        self.normal_table = PerformanceTable(
            [
                [0, 0.5, 1 - 5000 / 25000],
                [2 / 3, 0, 1 - 12000 / 25000],
                [1 / 3, 1, 1 - 8500 / 25000],
                [1, 0.5, 1 - 18635.2 / 25000],
            ],
            alternatives=self.alternatives,
            criteria=self.criteria,
            scales={
                criterion: QuantitativeScale.normal()
                for criterion in self.criteria
            },
        )
        self.bounds = {
            "c01": NominalScale(["*", "**", "***", "****"]),
            "c02": NominalScale(["Perfect", "Good", "Bad"]),
            "c03": QuantitativeScale(5000, 18635.2),
        }

    def test_constructor(self):
        assert_frame_equal(self.performance_table.df, self.df)
        self.assertEqual(self.performance_table.scales, self.scales)
        table = PerformanceTable(self.numeric_table.df)
        assert_frame_equal(table.df, self.numeric_table.df)
        self.assertEqual(table.bounds, table.scales)

    def test_equal(self):
        self.assertNotEqual(self.performance_table, self.df)
        self.assertNotEqual(self.performance_table, self.numeric_table)
        self.assertEqual(
            PerformanceTable(
                self.df, self.scales, self.alternatives, self.criteria
            ),
            self.performance_table,
        )

    def test_criteria(self):
        self.assertEqual(self.performance_table.criteria, self.criteria)

    def test_alternatives(self):
        self.assertEqual(
            self.performance_table.alternatives, self.alternatives
        )

    def test_alternatives_values(self):
        for alternative, alternative_values in zip(
            self.performance_table.alternatives,
            self.performance_table.alternatives_values,
        ):
            self.assertEqual(
                alternative_values,
                self.performance_table.get_alternative_values(alternative),
            )

    def test_criteria_values(self):
        for criterion, criterion_values in zip(
            self.performance_table.criteria,
            self.performance_table.criteria_values,
        ):
            self.assertEqual(
                criterion_values,
                self.performance_table.get_criterion_values(criterion),
            )

    def test_is_numeric(self):
        self.assertTrue(self.numeric_table.is_numeric)
        self.assertFalse(self.performance_table.is_numeric)

    def test_bounds(self):
        bounds = self.performance_table.bounds
        self.assertEqual(set(bounds.keys()), set(self.bounds.keys()))
        for criterion, scale in bounds.items():
            self.assertEqual(type(scale), type(self.bounds[criterion]))
            if isinstance(scale, QuantitativeScale):
                self.assertEqual(
                    [scale.dmin, scale.dmax, scale.preference_direction],
                    [
                        self.bounds[criterion].dmin,
                        self.bounds[criterion].dmax,
                        self.bounds[criterion].preference_direction,
                    ],
                )
            else:
                self.assertEqual(
                    set(scale.labels), set(self.bounds[criterion].labels)
                )

    def test_get_alternative_values(self):
        expected = ScaleValues(
            Series(["***", "Bad", 12000], index=self.criteria, name="a02"),
            self.scales,
        )
        res = self.performance_table.get_alternative_values("a02")
        self.assertEqual(expected.scales, res.scales)
        assert_series_equal(expected.data, res.data)

    def test_get_alternative_values_at(self):
        expected = ScaleValues(
            Series(["***", "Bad", 12000], index=self.criteria, name="a02"),
            self.scales,
        )
        res = self.performance_table.get_alternative_values_at(1)
        self.assertEqual(expected.scales, res.scales)
        assert_series_equal(expected.data, res.data)

    def test_get_criterion_values(self):
        expected = ScaleValues(
            Series(
                ["Good", "Bad", "Perfect", "Good"],
                index=self.alternatives,
                name="c02",
            ),
            self.scales["c02"],
        )
        res = self.performance_table.get_criterion_values("c02")
        self.assertEqual(expected.scales, res.scales)
        assert_series_equal(expected.data, res.data)

    def test_get_criterion_values_at(self):
        expected = ScaleValues(
            Series(
                ["Good", "Bad", "Perfect", "Good"],
                index=self.alternatives,
                name="c02",
            ),
            self.scales["c02"],
        )
        res = self.performance_table.get_criterion_values_at(1)
        self.assertEqual(expected.scales, res.scales)
        assert_series_equal(expected.data, res.data)

    def test_apply_criteria_functions(self):
        functions = {
            "c01": DiscreteFunction({"*": 0, "**": 1, "***": 2, "****": 3}),
            "c02": lambda x: f"Very {x}",
            "c03": lambda x: x * 2,
        }
        expected = PerformanceTable(
            [
                [0, "Very Good", 10000],
                [2, "Very Bad", 24000],
                [1, "Very Perfect", 17000],
                [3, "Very Good", 37270.4],
            ],
            scales=self.scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        res = self.performance_table.apply_criteria_functions(functions)
        assert_frame_equal(res.df, expected.df)
        self.assertEqual(res.scales, self.scales)

    def test_apply_criteria_weights(self):
        weights = {"c01": 1, "c02": 0.5, "c03": 2.0}
        res = self.numeric_table.apply_criteria_weights(weights)
        expected = PerformanceTable(
            [
                [1, 1, 10000],
                [3, 1.5, 24000],
                [2, 0.5, 17000],
                [4, 1, 37270.4],
            ],
            scales=self.numeric_scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        assert_frame_equal(res.df, expected.df, check_dtype=False)
        self.assertEqual(res.scales, self.numeric_scales)

    def test_is_within_criteria_scales(self):
        self.assertTrue(self.performance_table.is_within_criteria_scales)
        table = PerformanceTable(
            [
                ["*", "Good", 5000],
                ["Stars", "Bad", 12000],
                ["**", "Perfect", 8500],
                ["****", "Good", 18635.2],
            ],
            scales=self.scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        self.assertFalse(table.is_within_criteria_scales)

    def test_within_criteria_scales(self):
        res = self.performance_table.within_criteria_scales
        self.assertTrue(res.df.all(None))
        table = PerformanceTable(
            [
                ["*", "Good", 5000],
                ["Stars", "Bad", 12000],
                ["**", "Perfect", 8500],
                ["****", "Good", 18635.2],
            ],
            scales=self.scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        self.assertFalse(table.within_criteria_scales.df.loc["a02", "c01"])

    def test_transform(self):
        out_scales = {
            "c01": self.scales["c01"].quantitative,
            "c02": self.scales["c02"].quantitative,
            "c03": self.scales["c03"],
        }
        res = self.performance_table.transform(out_scales)
        assert_frame_equal(self.numeric_table.df, res.df, check_dtype=False)

    def test_normalize_without_scales(self):
        res = DataFrame(
            [
                [0, 0.5, 0],
                [2 / 3, 1, 7000 / 13635.2],
                [1 / 3, 0, 3500 / 13635.2],
                [1, 0.5, 1],
            ],
            index=self.alternatives,
            columns=self.criteria,
        )
        assert_frame_equal(
            self.numeric_table.normalize_without_scales().df, res
        )
        self.assertRaises(
            TypeError, self.performance_table.normalize_without_scales
        )

    def test_normalize(self):
        n = self.performance_table.normalize()
        assert_frame_equal(n.df, self.normal_table.df)
        self.assertEqual(n.scales, self.normal_table.scales)
        self.assertEqual(n, self.normal_table)
        table = PerformanceTable(self.numeric_table.df)
        self.assertEqual(table.normalize(), table.normalize_without_scales())

    def test_sum(self):
        self.assertEqual(
            self.performance_table.sum(),
            self.performance_table.df["c03"].sum(),
        )
        assert_series_equal(
            self.performance_table.sum(0),
            Series({"c03": self.performance_table.df["c03"].sum()}),
        )
        table = PerformanceTable([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5]])
        self.assertEqual(table.sum(), 30)

    def test_subtable(self):
        expected = PerformanceTable(
            [
                ["*", "Good", 5000],
                ["***", "Bad", 12000],
                ["**", "Perfect", 8500],
                ["****", "Good", 18635.2],
            ],
            scales=self.scales,
            alternatives=self.alternatives,
            criteria=self.criteria,
        )
        expected = PerformanceTable(
            [
                ["*", "Good"],
                ["**", "Perfect"],
            ],
            scales={"c01": self.scales["c01"], "c02": self.scales["c02"]},
            alternatives=["a01", "a03"],
            criteria=["c01", "c02"],
        )
        res = self.performance_table.subtable(["a01", "a03"], ["c02", "c01"])
        self.assertEqual(res, expected)

        self.assertEqual(
            self.performance_table.subtable(), self.performance_table
        )
