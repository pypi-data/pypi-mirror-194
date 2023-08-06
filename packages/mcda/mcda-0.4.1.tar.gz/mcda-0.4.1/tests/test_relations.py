import unittest

from pandas import Series
from pandas.testing import assert_frame_equal, assert_series_equal

from mcda.core.performance_table import Scores
from mcda.core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    OutrankingMatrix,
    PreferenceRelation,
    PreferenceStructure,
    Ranking,
    Relation,
)
from mcda.core.scales import PreferenceDirection, QuantitativeScale
from mcda.core.set_functions import HashableSet


class RelationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = Relation(0, 1)
        self.r2 = Relation(0, 1)
        self.r3 = Relation(1, 0)
        self.r4 = Relation(1, 2)

    def test_constructor(self):
        self.assertEqual((self.r1.a, self.r1.b), (0, 1))

    def test_repr(self):
        self.assertEqual(self.r1.__repr__(), "0  1")

    def test_elements(self):
        self.assertEqual(self.r1.elements, (0, 1))

    def test_same_elements(self):
        self.assertTrue(self.r1.same_elements(self.r2))
        self.assertTrue(self.r1.same_elements(self.r3))
        self.assertFalse(self.r1.same_elements(self.r4))

    def test_equal(self):
        self.assertEqual(self.r1, self.r2)
        self.assertNotEqual(self.r1, self.r3)
        self.assertNotEqual(self.r1, (0, 1))

    def test_add(self):
        self.assertRaises(TypeError, lambda r1, r2: r1 + r2, self.r1, (0, 1))
        self.assertTrue(isinstance(self.r1 + self.r4, PreferenceStructure))

    def test_hash(self):
        self.assertEqual(hash(self.r1), hash(self.r3))

    def test_compatible(self):
        self.assertTrue(self.r1.compatible(self.r2))
        self.assertFalse(self.r1.compatible(self.r3))
        self.assertTrue(self.r1.compatible(self.r4))

    def test_types(self):
        self.assertEqual(
            set(Relation.types()),
            {
                PreferenceRelation,
                IncomparableRelation,
                IndifferenceRelation,
            },
        )


class PreferenceRelationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = PreferenceRelation(0, 1)
        self.r2 = PreferenceRelation(1, 0)

    def test_constructor(self):
        self.assertRaises(ValueError, PreferenceRelation, 0, 0)

    def test_equal(self):
        self.assertNotEqual(self.r1, self.r2)
        self.assertNotEqual(self.r1, (0, 1))


class IndifferenceRelationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = IndifferenceRelation(0, 1)
        self.r2 = IndifferenceRelation(0, 0)
        self.r3 = IndifferenceRelation(1, 0)

    def test_equal(self):
        self.assertEqual(self.r1, self.r3)
        self.assertNotEqual(self.r1, (0, 1))


class IncomparableRelationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = IncomparableRelation(0, 1)
        self.r2 = IncomparableRelation(1, 0)

    def test_constructor(self):
        self.assertRaises(ValueError, IncomparableRelation, 0, 0)

    def test_equal(self):
        self.assertEqual(self.r1, self.r2)
        self.assertNotEqual(self.r1, (0, 1))


class PreferenceStructureTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.relations_list = [
            PreferenceRelation(1, 0),
            IndifferenceRelation(1, 2),
            PreferenceRelation(2, 3),
            IncomparableRelation(3, 4),
        ]
        self.relations = PreferenceStructure(self.relations_list)
        self.outranking_matrix = OutrankingMatrix(
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ]
        )
        self.transitive_closure = OutrankingMatrix(
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ]
        )
        self.transitive_reduction = PreferenceStructure(
            [
                PreferenceRelation(HashableSet((1, 2)), HashableSet((0,))),
                PreferenceRelation(HashableSet((1, 2)), HashableSet((3,))),
            ]
        )
        self.elements = [0, 1, 2, 3, 4]
        self.total_preorder = PreferenceStructure(
            [
                PreferenceRelation(0, 1),
                IndifferenceRelation(1, 2),
                PreferenceRelation(2, 3),
            ]
        )
        self.total_preorder_scores = Scores(Series([10, 5, 5, 0]))
        self.total_order = PreferenceStructure(
            [
                PreferenceRelation(0, 1),
                PreferenceRelation(1, 2),
                PreferenceRelation(2, 3),
            ]
        )

    def test_constructor(self):
        self.assertEqual(self.relations._relations, self.relations_list)
        self.assertEqual(
            PreferenceStructure(self.relations_list * 2)._relations,
            self.relations_list,
        )
        self.assertEqual(PreferenceStructure().relations, [])
        self.assertEqual(
            PreferenceStructure(self.relations).relations,
            self.relations.relations,
        )
        self.assertEqual(
            PreferenceStructure(PreferenceRelation(0, 1)).relations,
            [PreferenceRelation(0, 1)],
        )
        self.assertRaises(
            ValueError,
            PreferenceStructure,
            [PreferenceRelation(0, 1), PreferenceRelation(1, 0)],
        )
        self.assertRaises(
            ValueError, self.relations.__add__, PreferenceRelation(0, 1)
        )

    def test_elements(self):
        self.assertEqual(self.relations.elements, self.elements)

    def test_length(self):
        self.assertEqual(len(self.relations), len(self.relations_list))

    def test_repr(self):
        self.assertEqual(
            self.relations.__repr__(), "[1 P 0, 1 I 2, 2 P 3, 3 R 4]"
        )

    def test_add(self):
        r1 = self.relations + PreferenceRelation(4, 5)
        self.assertEqual(
            r1._relations, self.relations_list + [PreferenceRelation(4, 5)]
        )

        r2 = PreferenceStructure([PreferenceRelation(4, 5)])
        self.assertEqual(
            (self.relations + r2)._relations,
            self.relations_list + [PreferenceRelation(4, 5)],
        )

        r3 = [PreferenceRelation(4, 5)]
        self.assertEqual(
            (self.relations + r3)._relations,
            self.relations_list + [PreferenceRelation(4, 5)],
        )

    def test_is_total_preorder(self):
        self.assertFalse(self.relations.is_total_preorder)
        self.assertTrue(self.total_preorder.is_total_preorder)
        self.assertTrue(self.total_order.is_total_preorder)

    def test_is_total_order(self):
        self.assertFalse(self.relations.is_total_order)
        self.assertFalse(self.total_preorder.is_total_order)
        self.assertTrue(self.total_order.is_total_order)

    def test_equal(self):
        self.assertEqual(
            self.relations, PreferenceStructure(self.relations_list)
        )
        self.assertNotEqual(self.relations, self.relations_list)

    def test_getitem(self):
        self.assertEqual(
            self.relations[PreferenceRelation]._relations,
            [
                PreferenceRelation(1, 0),
                PreferenceRelation(2, 3),
            ],
        )
        self.assertEqual(self.relations[0, 1], PreferenceRelation(1, 0))
        self.assertIsNone(self.relations[0, 4])
        self.assertEqual(
            self.relations[1]._relations,
            [PreferenceRelation(1, 0), IndifferenceRelation(1, 2)],
        )

    def test_delitem(self):
        r = PreferenceStructure(self.relations)
        del r[1]
        self.assertEqual(
            r._relations,
            [PreferenceRelation(2, 3), IncomparableRelation(3, 4)],
        )

    def test_contains(self):
        self.assertTrue(PreferenceRelation(1, 0) in self.relations)
        self.assertFalse(PreferenceRelation(0, 2) in self.relations)

    def test_outranking_matrix(self):
        assert_frame_equal(
            self.relations.outranking_matrix.df, self.outranking_matrix.df
        )

    def test_from_outranking_matrix(self):
        r = PreferenceStructure.from_outranking_matrix(self.outranking_matrix)
        for rr in self.relations:
            self.assertTrue(rr in r)

    def test_transitive_closure(self):
        self.assertEqual(
            self.relations.transitive_closure,
            PreferenceStructure.from_outranking_matrix(
                self.transitive_closure
            ),
        )

    def test_transitive_reduction(self):
        res = self.relations.transitive_reduction[
            PreferenceRelation, IndifferenceRelation
        ]
        self.assertEqual(self.transitive_reduction, res)

    def test_from_scores(self):
        self.assertEqual(
            PreferenceStructure.from_scores(
                self.total_preorder_scores
            ).transitive_closure,
            self.total_preorder.transitive_closure,
        )

    def test_copy(self):
        r = self.relations.copy()
        self.assertEqual(r, self.relations)
        r += IndifferenceRelation(4, 5)
        self.assertNotEqual(r, self.relations)


class OutrankingMatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.relations = PreferenceStructure(
            [
                PreferenceRelation(1, 0),
                IndifferenceRelation(1, 2),
                PreferenceRelation(2, 3),
                IncomparableRelation(3, 4),
            ]
        )
        self.outranking_matrix = OutrankingMatrix(
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ]
        )

    def test_preference_structure(self):
        relations = self.outranking_matrix.preference_structure
        for r in self.relations:
            self.assertIn(r, relations)

    def test_from_preference_structure(self):
        self.assertEqual(
            OutrankingMatrix.from_preference_structure(self.relations),
            self.outranking_matrix,
        )

    def test_from_ranked_categories(self):
        categories = [[0, 1], [2], [3, 4]]
        expected = OutrankingMatrix(
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1],
            ]
        )
        self.assertEqual(
            OutrankingMatrix.from_ranked_categories(categories), expected
        )


class RankingTestCase(unittest.TestCase):
    def setUp(self):
        self.data = Series([0, 1, 2])
        self.ranking = Ranking(self.data)

    def test_constructor(self):
        self.assertEqual(
            self.ranking.scales,
            {
                k: QuantitativeScale(0, 2, PreferenceDirection.MIN)
                for k in range(3)
            },
        )

    def test_copy(self):
        copy = self.ranking.copy()
        assert_series_equal(copy.data, self.ranking.data)
        self.assertEqual(copy.scales, self.ranking.scales)
