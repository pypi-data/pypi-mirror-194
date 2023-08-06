import unittest

from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal, assert_series_equal

from mcda.core.performance_table import PerformanceTable
from mcda.core.relations import (
    IndifferenceRelation,
    OutrankingMatrix,
    PreferenceRelation,
    PreferenceStructure,
    Ranking,
)
from mcda.core.scales import (
    PreferenceDirection,
    QualitativeScale,
    QuantitativeScale,
)
from mcda.outranking.srmp import SRMP, SRMPTrainer


class TestSRMPTrainer(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(0, 1),
            1: QuantitativeScale(3, 4),
            2: QuantitativeScale(1, 2),
            3: QuantitativeScale(0, 1),
            4: QuantitativeScale(30, 100, PreferenceDirection.MIN),
        }
        self.table = PerformanceTable(
            [
                [0.720, 3.560, 1.340, 0.62, 44.340],
                [0.8, 3.940, 1.430, 0.74, 36.360],
                [0.760, 3.630, 1.380, 0.89, 48.750],
                [0.780, 3.740, 1.450, 0.72, 42.130],
                [0.740, 3.540, 1.370, 0.73, 36.990],
                [0.690, 3.740, 1.450, 0.84, 42.430],
                [0.7, 3.280, 1.280, 0.83, 47.430],
                [0.860, 3.370, 1.150, 0.8, 80.790],
            ],
            scales=self.scales,
        )
        self.relations = PreferenceStructure(
            [
                PreferenceRelation(1, 0),
                PreferenceRelation(3, 2),
                PreferenceRelation(3, 4),
                PreferenceRelation(5, 4),
                PreferenceRelation(5, 6),
                IndifferenceRelation(6, 7),
                IndifferenceRelation(7, 0),
                IndifferenceRelation(6, 0),
                PreferenceRelation(1, 3),
                PreferenceRelation(2, 6),
            ]
        )
        self.lexicographic_order = [1, 0]
        self.trainer = SRMPTrainer(
            self.table,
            self.relations,
            3,
            inconsistencies=True,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )

    def test_constructor(self):
        self.assertEqual(self.trainer.performance_table, self.table)
        self.assertEqual(self.trainer.relations, self.relations)
        self.assertEqual(self.trainer.max_profiles_number, 3)
        self.assertIsNone(self.trainer.profiles_number)
        self.assertIsNone(self.trainer.lexicographic_order)
        self.assertEqual(self.trainer.inconsistencies, True)
        self.assertEqual(self.trainer.gamma, 0.1)
        self.assertEqual(self.trainer.non_dictator, True)
        self.assertEqual(self.trainer.solver_args, {})

        self.assertRaises(ValueError, SRMPTrainer, self.table, self.relations)

    def test_denormalize_value(self):
        x = 0.51
        scale = QuantitativeScale(1, 3)
        denormalized_value = 2.02
        calculated_denormalized_value = SRMPTrainer._denormalize_value(
            x, scale
        )
        self.assertEqual(denormalized_value, calculated_denormalized_value)

        x = 0.51
        scale = QuantitativeScale(1, 3, PreferenceDirection.MIN)
        denormalized_value = 1.98
        calculated_denormalized_value = SRMPTrainer._denormalize_value(
            x, scale
        )
        self.assertEqual(denormalized_value, calculated_denormalized_value)

        x = 0.51
        scale = QualitativeScale(Series({"Evil": 1, "Neutral": 2, "Good": 3}))
        denormalized_value = "Good"
        calculated_denormalized_value = SRMPTrainer._denormalize_value(
            x, scale
        )
        self.assertEqual(denormalized_value, calculated_denormalized_value)

    def test_denormalize(self):
        res = SRMPTrainer._denormalize(self.table.normalize(), self.scales)
        assert_frame_equal(
            self.table.df,
            res.df,
        )
        self.assertEqual(self.scales, res.scales)

        scale = QualitativeScale(
            Series({"Evil": 0, "Neutral": 0.5, "Good": 1})
        )
        modified_scales = self.scales.copy()
        modified_scales[0] = scale
        modified_dataset = PerformanceTable(
            self.table.df.copy(deep=True), scales=modified_scales
        )
        modified_dataset.df[0] = [
            "Evil",
            "Neutral",
            "Good",
            "Evil",
            "Neutral",
            "Good",
            "Evil",
            "Neutral",
        ]
        modified_norm_dataset = modified_dataset.normalize()

        assert_frame_equal(
            modified_dataset.df,
            SRMPTrainer._denormalize(
                modified_norm_dataset, modified_scales
            ).df,
        )

        modified_norm_dataset.df.iat[0, 0] = 0.1
        modified_dataset.df.iat[0, 0] = "Neutral"

        assert_frame_equal(
            modified_dataset.df,
            SRMPTrainer._denormalize(
                modified_norm_dataset, modified_scales
            ).df,
        )

    def test_train_lexicographic_order(self):
        srmp, prob = self.trainer._train_lexicographic_order(
            self.lexicographic_order
        )
        fitness = self.trainer.compute_fitness(prob, len(self.relations), True)
        # Check no dictator criterion exists
        for w in srmp.criteria_weights.values():
            self.assertTrue(w <= 0.5)
        self.assertEqual(type(srmp), SRMP)
        self.assertEqual(fitness, 0.9)
        self.assertEqual(srmp.lexicographic_order, self.lexicographic_order)
        self.assertEqual(
            srmp.criteria_weights, {0: 0.1, 1: 0.2, 2: 0.5, 3: 0.1, 4: 0.1}
        )
        assert_frame_equal(
            srmp.category_profiles.df,
            DataFrame(
                [
                    [0.00, 3.73, 1.55, 0.0, 99.36],
                    [0.69, 3.94, 2.00, 1.0, 80.79],
                ]
            ),
            atol=0.01,
        )

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            lexicographic_order=self.lexicographic_order,
            inconsistencies=True,
            gamma=0.1,
            non_dictator=False,
            solver_args={},
        )
        srmp, prob = trainer._train_lexicographic_order(
            self.lexicographic_order
        )
        self.assertEqual(
            srmp.criteria_weights, {0: 0.6, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1}
        )

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            lexicographic_order=self.lexicographic_order,
            inconsistencies=False,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )
        srmp, prob = trainer._train_lexicographic_order(
            self.lexicographic_order
        )
        self.assertIsNone(srmp)
        self.assertEqual(
            trainer.compute_fitness(prob, len(self.relations), False), 0
        )

    def test_train(self):
        srmp = self.trainer.train()
        self.assertEqual(self.trainer.fitness, 1.0)
        # Check no dictator criterion exists
        for w in srmp.criteria_weights.values():
            self.assertTrue(w <= 0.5)
        rank = srmp(self.table)
        exp_rank = Ranking(
            Series([4, 1, 3, 2, 3, 2, 4, 4]),
        )
        assert_series_equal(exp_rank.data, rank.data)

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            profiles_number=3,
            inconsistencies=True,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )
        srmp2 = trainer.train()
        rank = srmp2(self.table)
        assert_series_equal(exp_rank.data, rank.data)

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            lexicographic_order=[0, 1, 2],
            inconsistencies=True,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )
        srmp3 = trainer.train()
        rank = srmp3(self.table)
        assert_series_equal(exp_rank.data, rank.data)

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            lexicographic_order=self.lexicographic_order,
            inconsistencies=False,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )
        srmp4 = trainer.train()
        self.assertIsNone(srmp4)

        trainer = SRMPTrainer(
            self.table,
            self.relations,
            max_profiles_number=2,
            inconsistencies=False,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )
        srmp5 = trainer.train()
        self.assertIsNone(srmp5)

        self.assertRaises(ValueError, self.trainer._train)


class TestSRMP(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(0, 1),
            1: QuantitativeScale(3, 4),
            2: QuantitativeScale(1, 2),
            3: QuantitativeScale(0, 1),
            4: QuantitativeScale(30, 100, PreferenceDirection.MIN),
        }
        self.table = PerformanceTable(
            [
                [0.720, 3.560, 1.340, 0.62, 44.340],
                [0.8, 3.940, 1.430, 0.74, 36.360],
                [0.760, 3.630, 1.380, 0.89, 48.750],
                [0.780, 3.740, 1.450, 0.72, 42.130],
                [0.740, 3.540, 1.370, 0.73, 36.990],
                [0.690, 3.740, 1.450, 0.84, 42.430],
                [0.7, 3.280, 1.280, 0.83, 47.430],
                [0.860, 3.370, 1.150, 0.8, 80.790],
            ],
            scales=self.scales,
        )
        self.weights = {0: 30, 1: 30, 2: 20, 3: 10, 4: 10}
        self.profiles = PerformanceTable(
            [
                [0.750, 3.500, 1.300, 0.730, 43.00],
                [0.800, 3.700, 1.370, 0.790, 42.000],
            ]
        )
        self.lexicographic_order = [1, 0]
        self.srmp = SRMP(self.weights, self.profiles, self.lexicographic_order)
        self.outranking_matrices = [
            OutrankingMatrix(
                [
                    [1, 0, 0, 0, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 1, 1],
                ]
            ),
            OutrankingMatrix(
                [
                    [1, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 1, 1, 0, 1, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [1, 0, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0, 1, 1],
                ]
            ),
        ]
        self.rank = Ranking(
            Series([8, 1, 5, 3, 6, 2, 7, 4]),
        )

    def test_constructor(self):
        self.assertEqual(self.srmp.criteria_weights, self.weights)
        self.assertEqual(self.srmp.category_profiles, self.profiles)
        self.assertEqual(
            self.srmp.lexicographic_order, self.lexicographic_order
        )

    def test_outranking(self):
        self.assertEqual(
            self.outranking_matrices, self.srmp.construct(self.table)
        )

    def test_exploit(self):
        assert_series_equal(
            self.rank.data, self.srmp.exploit(self.outranking_matrices).data
        )

    def test_call(self):
        assert_series_equal(self.rank.data, self.srmp(self.table).data)

    def test_train(self):
        """
        .. todo:: replace SRMPTrainer.train subcall by a mockup patch
        """
        relations = PreferenceStructure(
            [
                PreferenceRelation(1, 0),
                PreferenceRelation(3, 2),
                PreferenceRelation(3, 4),
                PreferenceRelation(5, 4),
                PreferenceRelation(5, 6),
                IndifferenceRelation(6, 7),
                IndifferenceRelation(7, 0),
                IndifferenceRelation(6, 0),
                PreferenceRelation(1, 3),
                PreferenceRelation(2, 6),
            ]
        )
        srmp = SRMP.train(
            self.table,
            relations,
            max_profiles_number=3,
            inconsistencies=True,
            gamma=0.1,
            non_dictator=True,
            solver_args=None,
        )

        # Check no dictator criterion exists
        for w in srmp.criteria_weights.values():
            self.assertTrue(w <= 0.5)
        rank = srmp(self.table)
        exp_rank = Ranking(
            Series([4, 1, 3, 2, 3, 2, 4, 4]),
        )
        assert_series_equal(exp_rank.data, rank.data)
