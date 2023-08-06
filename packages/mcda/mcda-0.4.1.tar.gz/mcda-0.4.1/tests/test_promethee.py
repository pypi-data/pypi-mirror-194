import unittest
from math import exp

from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal, assert_series_equal

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    PreferenceRelation,
    PreferenceStructure,
)
from mcda.core.scales import PreferenceDirection, QuantitativeScale
from mcda.outranking.promethee import (
    GaussianFunction,
    LevelFunction,
    LinearFunction,
    Promethee1,
    Promethee2,
    PrometheeGaia,
    UShapeFunction,
    UsualFunction,
    VShapeFunction,
)


class TestUShapeFunction(unittest.TestCase):
    def setUp(self):
        self.q = 1
        self.function = UShapeFunction(self.q)

    def test(self):
        self.assertEqual(self.function.q, self.q)
        self.assertEqual(self.function(-1), 0)
        self.assertEqual(self.function(1.5), 1)


class TestUsualFunction(unittest.TestCase):
    def setUp(self):
        self.function = UsualFunction()

    def test(self):
        self.assertEqual(self.function.q, 0)
        self.assertEqual(self.function(-1), 0)
        self.assertEqual(self.function(0.5), 1)


class TestVShapeFunction(unittest.TestCase):
    def setUp(self):
        self.p = 1
        self.function = VShapeFunction(self.p)

    def test(self):
        self.assertEqual(self.function.p, self.p)
        self.assertEqual(self.function(-1), 0)
        self.assertEqual(self.function(1.5), 1)
        self.assertEqual(self.function(0.5), 0.5)


class TestLevelFunction(unittest.TestCase):
    def setUp(self):
        self.p = 2
        self.q = 1
        self.function = LevelFunction(self.p, self.q)

    def test(self):
        self.assertRaises(ValueError, LevelFunction, 1, 2)
        self.assertEqual(self.function.q, self.q)
        self.assertEqual(self.function.p, self.p)
        self.assertEqual(self.function(0.5), 0)
        self.assertEqual(self.function(1.5), 0.5)
        self.assertEqual(self.function(2.5), 1)


class TestLinearFunction(unittest.TestCase):
    def setUp(self):
        self.p = 2
        self.q = 1
        self.function = LinearFunction(self.p, self.q)

    def test(self):
        self.assertEqual(self.function.q, self.q)
        self.assertEqual(self.function.p, self.p)
        self.assertEqual(self.function(0.5), 0)
        self.assertEqual(self.function(1.5), 0.5)
        self.assertEqual(self.function(2.5), 1)


class TestGaussianFunction(unittest.TestCase):
    def setUp(self):
        self.s = 1
        self.function = GaussianFunction(self.s)

    def test(self):
        self.assertEqual(self.function.s, self.s)
        self.assertEqual(self.function(-1), 0)
        self.assertEqual(self.function(1), 1 - exp(-1 / 2))


class TestPromethee1(unittest.TestCase):
    def setUp(self):
        self.weights = {0: 0.5, 1: 3, 2: 1.5, 3: 0.2, 4: 2, 5: 1}
        self.functions = {
            0: UsualFunction(),
            1: UShapeFunction(2.5),
            2: VShapeFunction(3),
            3: LevelFunction(1, 0.5),
            4: LinearFunction(2, 1),
            5: GaussianFunction(1),
        }
        scales = {
            0: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            1: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            2: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            3: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            4: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            5: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
        }
        self.table = PerformanceTable(
            [
                [1, 2, -1, 5, 2, 2],  # a1
                [3, 5, 3, -5, 3, 3],  # a2
                [3, -5, 3, 4, 3, 2],  # a3
                [2, -2, 2, 5, 1, 1],  # a4
                [3, 5, 3, -5, 3, 3],  # a5
            ],
            scales=scales,
        )
        self.promethee = Promethee1(self.weights, self.functions)

    def test_constructor(self):
        self.assertEqual(self.promethee.criteria_weights, self.weights)
        self.assertEqual(self.promethee.preference_functions, self.functions)

    def test_adapt_performance_table(self):
        table = PerformanceTable(
            self.table.df,
            scales={
                0: QuantitativeScale(-5, 5, PreferenceDirection.MIN),
                1: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
                2: QuantitativeScale(-5, 5, PreferenceDirection.MIN),
                3: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
                4: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
                5: QuantitativeScale(-5, 5, PreferenceDirection.MIN),
            },
        )
        expected_dataset = DataFrame(
            [
                [-1, 2, 1, 5, 2, -2],  # a1
                [-3, 5, -3, -5, 3, -3],  # a2
                [-3, -5, -3, 4, 3, -2],  # a3
                [-2, -2, -2, 5, 1, -1],  # a4
                [-3, 5, -3, -5, 3, -3],  # a5
            ]
        )
        assert_frame_equal(
            self.promethee.adapt_performance_table(table).df,
            expected_dataset,
            check_dtype=False,
        )

    def test_outranking_flows(self):
        matrix = self.promethee.multicriteria_preference_degree(self.table)

        pos_flows = self.promethee.outranking_flows(matrix)
        result = Series([0.84607, 1.90874, 0.70652, 0.67073, 1.90874])
        assert_series_equal(pos_flows, result, atol=0.01)

        neg_flows = self.promethee.outranking_flows(matrix, negative=True)
        result = Series([1.80328, 0.07317, 1.58378, 2.50200, 0.07317])
        assert_series_equal(neg_flows, result, atol=0.01)

    def test_call(self):
        relations = self.promethee(self.table)
        expected_relations = PreferenceStructure(
            [
                PreferenceRelation(1, 0),
                IncomparableRelation(0, 2),
                PreferenceRelation(0, 3),
                PreferenceRelation(4, 0),
                PreferenceRelation(1, 2),
                PreferenceRelation(1, 3),
                IndifferenceRelation(1, 4),
                PreferenceRelation(2, 3),
                PreferenceRelation(4, 2),
                PreferenceRelation(4, 3),
            ]
        )
        self.assertEqual(relations, expected_relations)


class TestPromethee2(unittest.TestCase):
    def setUp(self):
        self.weights = {0: 0.5, 1: 3, 2: 1.5, 3: 0.2, 4: 2, 5: 1}
        self.functions = {
            0: UsualFunction(),
            1: UShapeFunction(2.5),
            2: VShapeFunction(3),
            3: LevelFunction(1, 0.5),
            4: LinearFunction(2, 1),
            5: GaussianFunction(1),
        }
        scales = {
            0: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            1: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            2: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            3: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            4: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            5: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
        }
        self.table = PerformanceTable(
            [
                [1, 2, -1, 5, 2, 2],  # a1
                [3, 5, 3, -5, 3, 3],  # a2
                [3, -5, 3, 4, 3, 2],  # a3
                [2, -2, 2, 5, 1, 1],  # a4
                [3, 5, 3, -5, 3, 3],  # a5
            ],
            scales=scales,
        )
        self.promethee = Promethee2(self.weights, self.functions)

    def test_call(self):
        res = self.promethee(self.table)
        check_val = ScaleValues(
            Series([-0.96261, 1.83557, -0.87726, -1.83127, 1.83557])
        )
        assert_series_equal(res.data, check_val.data)


class TestPrometheeGaia(unittest.TestCase):
    def setUp(self):
        self.weights = {0: 0.5, 1: 3, 2: 1.5, 3: 0.2, 4: 2, 5: 1}
        self.functions = {
            0: UsualFunction(),
            1: UShapeFunction(2.5),
            2: VShapeFunction(3),
            3: LevelFunction(1, 0.5),
            4: LinearFunction(2, 1),
            5: GaussianFunction(1),
        }
        scales = {
            0: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            1: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            2: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            3: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            4: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
            5: QuantitativeScale(-5, 5, PreferenceDirection.MAX),
        }
        self.table = PerformanceTable(
            [
                [1, 2, -1, 5, 2, 2],  # a1
                [3, 5, 3, -5, 3, 3],  # a2
                [3, -5, 3, 4, 3, 2],  # a3
                [2, -2, 2, 5, 1, 1],  # a4
                [3, 5, 3, -5, 3, 3],  # a5
            ],
            scales=scales,
        )
        self.promethee = PrometheeGaia(self.weights, self.functions)

    def test_unicriterion_net_flow_matrix(self):
        matrix = self.promethee.unicriterion_net_flows_matrix(self.table)
        dataset = DataFrame(
            [
                [-4, 0, -4.0, 2.5, 0.0, -0.393469],
                [2, 3, 1.333333, -3.0, 1.0, 1.651603],
                [2, -4, 1.333333, 1.0, 1.0, -0.393469],
                [-2, -2, 1.110223e-16, 2.5, -3.0, -2.516268],
                [2, 3, 1.333333, -3.0, 1.0, 1.651603],
            ]
        )
        assert_frame_equal(matrix, dataset, check_dtype=False)
