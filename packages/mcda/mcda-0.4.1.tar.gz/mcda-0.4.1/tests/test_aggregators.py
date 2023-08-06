import unittest
from math import log

from pandas import Series
from pandas.testing import assert_series_equal

from mcda.core.functions import FuzzyNumber
from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.scales import FuzzyScale, QuantitativeScale
from mcda.core.set_functions import Capacity, MobiusCapacity
from mcda.mavt.aggregators import (
    OWA,
    ULOWA,
    ChoquetIntegral,
    UtilityFunction,
    WeightedSum,
)


class WeightedSumTestCase(unittest.TestCase):
    def setUp(self):
        self.table = PerformanceTable(
            [[0, 1, 2, 3], [4, 5, 6, 7]],
            alternatives=["a01", "a02"],
            criteria=["c01", "c02", "c03", "c04"],
        )
        self.weights = {"c01": 1, "c02": 2, "c03": 1, "c04": 4}
        self.aggregator = WeightedSum(self.weights)

    def test_constructor(self):
        self.assertEqual(dict(self.aggregator.criteria_weights), self.weights)

    def test_call(self):
        res = Series({"a01": 16, "a02": 48})
        assert_series_equal(self.aggregator(self.table), res)
        assert_series_equal(self.aggregator(self.table.df), res)
        self.assertEqual(
            self.aggregator(self.table.get_alternative_values("a01")),
            res["a01"],
        )


class ChoquetIntegralTestCase(unittest.TestCase):
    def setUp(self):
        # Value taken from R kappalab package (7 digits accuracy)
        self.capacity = Capacity(
            [
                0.0,
                0.07692307692307693,
                0.15384615384615385,
                0.38461538461538464,
                0.23076923076923078,
                0.46153846153846156,
                0.6153846153846154,
                0.8461538461538461,
                0.3076923076923077,
                0.5384615384615384,
                0.6923076923076923,
                0.9230769230769231,
                0.7692307692307693,
                1.0,
                1,
                1,
            ]
        )
        self.mobius = MobiusCapacity(
            [
                0,
                0.07692308,
                0.15384615,
                0.15384615,
                0.23076923,
                0.15384615,
                0.23076923,
                -0.15384615,
                0.30769231,
                0.15384615,
                0.23076923,
                -0.15384615,
                0.23076923,
                -0.15384615,
                -0.38461538,
                -0.07692308,
            ]
        )
        self.values = Series([0.1, 0.9, 0.3, 0.8])
        self.choquet = 0.6615385

    def test_choquet_integral_capacity(self):
        choquet = ChoquetIntegral(self.capacity)
        self.assertAlmostEqual(choquet(self.values), self.choquet)

    def test_choquet_integral_mobius(self):
        choquet = ChoquetIntegral(self.mobius)
        self.assertAlmostEqual(choquet(self.values), self.choquet)


class OWATestCase(unittest.TestCase):
    def setUp(self):
        self.weights = [0.2, 0.3, 0.1, 0.4]
        self.owa = OWA(self.weights)

    def test_constructor(self):
        self.assertEqual(self.owa.weights, self.weights)

    def test_call(self):
        self.assertEqual(self.owa(Series([0.6, 1.0, 0.3, 0.5])), 0.55)

    def test_orness(self):
        self.assertEqual(OWA([1, 0, 0, 0, 0]).orness, 1)
        self.assertEqual(OWA([0, 0, 0, 1]).orness, 0)
        self.assertEqual(OWA([1 / 4, 1 / 4, 1 / 4, 1 / 4]).orness, 0.5)

    def test_andness(self):
        self.assertEqual(OWA([1, 0, 0, 0, 0]).andness, 0)
        self.assertEqual(OWA([0, 0, 0, 1]).andness, 1)
        self.assertEqual(OWA([1 / 4, 1 / 4, 1 / 4, 1 / 4]).andness, 0.5)

    def test_dispersion(self):
        self.assertEqual(OWA([0, 1, 0, 0]).dispersion, 0)
        self.assertEqual(OWA([1 / 4, 1 / 4, 1 / 4, 1 / 4]).dispersion, log(4))

    def test_divergence(self):
        self.assertEqual(OWA([1 / 2, 0, 0, 1 / 2]).divergence, 0.25)
        self.assertEqual(OWA([0, 0, 1 / 2, 0, 1 / 2, 0, 0]).divergence, 1 / 36)

    def test_balance(self):
        self.assertEqual(OWA([1, 0, 0, 0, 0]).balance, 1)
        self.assertEqual(OWA([0, 0, 0, 1]).balance, -1)
        self.assertEqual(OWA([1 / 4, 1 / 4, 1 / 4, 1 / 4]).balance, 0)

    def test_quantifier(self):
        self.assertEqual(OWA([0, 0, 1]).quantifier, [0, 0, 0, 1])
        self.assertEqual(OWA([1, 0, 0]).quantifier, [0, 1, 1, 1])

    def test_from_quantifier(self):
        self.assertEqual(OWA.from_quantifier([0, 1, 1]).weights, [1, 0])
        self.assertEqual(OWA.from_quantifier([0, 1, 1]).quantifier, [0, 1, 1])

    def test_and_aggregator(self):
        self.assertEqual(OWA.and_aggregator(5).weights, [0, 0, 0, 0, 1])

    def test_or_aggregator(self):
        self.assertEqual(OWA.or_aggregator(3).weights, [1, 0, 0])


class TestUlowa(unittest.TestCase):
    def setUp(self):
        self.fuzzy_sets = [
            FuzzyNumber([0, 0, 0, 0]),
            FuzzyNumber([0.0, 0.0, 0.0, 2.0]),
            FuzzyNumber([0.0, 2.0, 2.0, 5.0]),
            FuzzyNumber([2.0, 5.0, 5.0, 6.0]),
            FuzzyNumber([5.0, 6.0, 6.0, 7.0]),
            FuzzyNumber([6.0, 7.0, 8.0, 9.0]),
            FuzzyNumber([8.0, 9.0, 9.0, 10.0]),
            FuzzyNumber([9.0, 10.0, 10.0, 10.0]),
            FuzzyNumber([10, 10, 10, 10]),
        ]
        self.labels = ["N", "VL", "L", "M", "AH", "H", "VH", "P", "PP"]
        self.scale = FuzzyScale(Series(self.fuzzy_sets, index=self.labels))
        self.weights = [0.0, 0.0, 0.5, 0.5, 0.0]
        self.performance_table = PerformanceTable(
            [
                ["VL", "VL", "P", "H", "VL"],
                ["VL", "VL", "H", "P", "P"],
                ["VL", "VL", "L", "M", "L"],
                ["VH", "L", "H", "H", "AH"],
                ["P", "L", "H", "L", "AH"],
                ["P", "VL", "VL", "M", "AH"],
            ]
        )
        self.ulowa = ULOWA(self.weights, self.scale)

    def test_constructor(self):
        self.assertEqual(self.ulowa.weights, self.weights)
        self.assertEqual(self.ulowa.scale, self.scale)

    def test_delta(self):
        self.assertEqual(ULOWA.delta("N", "PP", 0.5, self.scale), 5.0)

    def test_most_similar(self):
        self.assertEqual(
            ULOWA.most_similar(
                "VL", "H", FuzzyNumber([5.5, 6.1, 6.5, 7.5]), self.scale
            ),
            "AH",
        )
        self.assertEqual(
            ULOWA.most_similar(
                "VL", "M", FuzzyNumber([5.5, 6.1, 6.5, 7.5]), self.scale
            ),
            "M",
        )

    def test_call(self):
        previsions = Series(["VL", "M", "VL", "AH", "M", "L"])
        assert_series_equal(self.ulowa(self.performance_table), previsions)
        self.assertRaises(ValueError, self.ulowa, Series([], dtype="float64"))


class TestUtilityFunction(unittest.TestCase):
    def setUp(self):
        self.functions = {0: lambda x: x * 2, 1: lambda x: -2 * x + 50}
        self.scales = {
            0: QuantitativeScale(-1, 1),
            1: QuantitativeScale(0, 100),
        }
        self.agg = UtilityFunction(self.functions, self.scales)

    def test_constructor(self):
        self.assertEqual(self.agg.criteria_functions, self.functions)
        self.assertEqual(self.agg.scales, self.scales)
        u = UtilityFunction(self.functions)
        self.assertEqual(
            u.scales,
            {c: QuantitativeScale.normal() for c in self.scales.keys()},
        )

    def test_call(self):
        s = Series([1, 10])
        table = PerformanceTable([[1, 10]], scales=self.scales)
        self.assertEqual(self.agg(s), 32)
        assert_series_equal(
            self.agg(table.df), Series([32]), check_dtype=False
        )
        assert_series_equal(self.agg(table), Series([32]), check_dtype=False)
        values = ScaleValues(
            Series([1, 0]),
            scales={
                0: QuantitativeScale.normal(),
                1: QuantitativeScale.normal(),
            },
        )
        self.assertEqual(self.agg(values), 52)
