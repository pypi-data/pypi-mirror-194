import unittest

from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal, assert_series_equal

from mcda.core.performance_table import PerformanceTable
from mcda.core.relations import OutrankingMatrix
from mcda.core.scales import PreferenceDirection, QuantitativeScale
from mcda.outranking.electre import Electre1, Electre2, Electre3, ElectreTri


class TestElectre1(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(1, 5, PreferenceDirection.MIN),
            1: QuantitativeScale(1, 5),
            2: QuantitativeScale(1, 5),
            3: QuantitativeScale(1, 5),
            4: QuantitativeScale(1, 5),
            5: QuantitativeScale(1, 5),
            6: QuantitativeScale(1, 5),
        }
        self.table = PerformanceTable(
            [
                [4, 2, 1, 5, 2, 2, 4],
                [3, 5, 3, 5, 3, 3, 3],
                [3, 5, 3, 5, 3, 2, 2],
                [4, 2, 2, 5, 1, 1, 1],
                [4, 1, 3, 5, 4, 1, 5],
            ],
            scales=self.scales,
        )
        self.weights = {
            0: 0.780,
            1: 1.180,
            2: 1.570,
            3: 3.140,
            4: 2.350,
            5: 0.390,
            6: 0.590,
        }
        self.c_hat = 0.75
        self.d_hat = 0.50
        self.electre = Electre1(self.weights, self.c_hat, self.d_hat)

    def test_constructor(self):
        self.assertEqual(self.electre.criteria_weights, self.weights)
        self.assertEqual(self.electre.c_hat, self.c_hat)
        self.assertEqual(self.electre.d_hat, self.d_hat)

    def test_concordance(self):
        concordance_matrix = DataFrame(
            [
                [1.0, 0.37, 0.41, 0.84, 0.55],
                [0.94, 1.0, 1.0, 1.0, 0.71],
                [0.94, 0.9, 1.0, 1.0, 0.71],
                [0.67, 0.31, 0.31, 1.0, 0.55],
                [0.84, 0.77, 0.77, 0.88, 1.0],
            ]
        )
        # Absolute value = 0.006 according to usual math rounding method
        # (if last digit >5 => round to superior else otherwise
        assert_frame_equal(
            self.electre.concordance(self.table),
            concordance_matrix,
            atol=0.006,
        )

    def test_discordance(self):
        discordance_matrix = DataFrame(
            [
                [0.0, 0.75, 0.75, 0.25, 0.5],
                [0.25, 0.0, 0.0, 0.0, 0.5],
                [0.5, 0.25, 0.0, 0.0, 0.75],
                [0.75, 0.75, 0.75, 0.0, 1.0],
                [0.25, 1.0, 1.0, 0.25, 0.0],
            ]
        )

        assert_frame_equal(
            self.electre.discordance(self.table), discordance_matrix
        )

    def test_outranking(self):
        outranking_matrix = OutrankingMatrix(
            [
                [1, 0, 0, 1, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 0, 1, 1],
            ]
        )
        self.assertEqual(
            self.electre.outranking(
                self.electre.concordance(self.table),
                self.electre.discordance(self.table),
            ),
            outranking_matrix,
        )

    def test_call(self):
        self.assertEqual(set(self.electre(self.table)), {0, 1, 2, 3, 4})
        self.assertEqual(
            set(self.electre(self.table, cycle_reduction=True)), {1, 2, 4}
        )
        self.assertEqual(
            set(self.electre(self.table, transitivity=True)), {0, 1, 2, 3, 4}
        )
        self.assertEqual(
            set(
                self.electre(
                    self.table, cycle_reduction=True, transitivity=True
                )
            ),
            {1, 2, 4},
        )


class TestElectre2(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(1, 5),
            1: QuantitativeScale(1, 5),
            2: QuantitativeScale(1, 5),
            3: QuantitativeScale(1, 5),
            4: QuantitativeScale(1, 5),
            5: QuantitativeScale(1, 5),
            6: QuantitativeScale(1, 5),
        }
        self.table = PerformanceTable(
            [
                [1, 2, 1, 5, 2, 2, 4],
                [3, 5, 3, 5, 3, 3, 3],
                [3, 5, 3, 5, 3, 2, 2],
                [1, 2, 2, 5, 1, 1, 1],
                [1, 1, 3, 5, 4, 1, 5],
            ],
            self.scales,
        )
        self.weights = {
            0: 0.0780,
            1: 0.1180,
            2: 0.1570,
            3: 0.3140,
            4: 0.2350,
            5: 0.0390,
            6: 0.0590,
        }
        self.c_hat = (0.65, 0.85)
        self.d_hat = (0.25, 0.50)
        self.electre = Electre2(self.weights, self.c_hat, self.d_hat)

    def test_constructor(self):
        self.assertEqual(self.electre.criteria_weights, self.weights)
        self.assertEqual(self.electre.c_hat, self.c_hat)
        self.assertEqual(self.electre.d_hat, self.d_hat)

    def test_outranking(self):
        s_outranking_matrix = OutrankingMatrix(
            [
                [1.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        w_outranking_matrix = OutrankingMatrix(
            [
                [1.0, 0.0, 0.0, 1.0, 0.0],
                [1.0, 1.0, 1.0, 1.0, 0.0],
                [1.0, 0.0, 1.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0],
                [1.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )

        concordance_mat = self.electre.concordance(self.table)
        discordance_mat = self.electre.discordance(self.table)

        self.assertEqual(
            self.electre.outranking(concordance_mat, discordance_mat),
            s_outranking_matrix,
        )
        self.assertEqual(
            self.electre.outranking(
                concordance_mat, discordance_mat, self.c_hat[0], self.d_hat[1]
            ),
            w_outranking_matrix,
        )

    def test_distillation(self):
        desc_distillate = [[1, 4], [2], [0], [3]]
        asc_distillate = [[1], [2, 4], [0], [3]]
        self.assertEqual(
            self.electre.distillation(*self.electre.construct(self.table)),
            desc_distillate,
        )
        self.assertEqual(
            self.electre.distillation(
                *self.electre.construct(self.table), ascending=True
            ),
            asc_distillate,
        )

    def test_call(self):
        final_rank = OutrankingMatrix(
            [
                [1, 0, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 0, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 1],
            ]
        )
        self.assertEqual(self.electre(self.table), final_rank)


class TestElectre3(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(7, 10),
            1: QuantitativeScale(7, 10),
            2: QuantitativeScale(5, 9),
            3: QuantitativeScale(6, 9),
        }
        self.table = PerformanceTable(
            [
                [8.84, 8.79, 6.43, 6.95],
                [8.57, 8.51, 5.47, 6.91],
                [7.76, 7.75, 5.34, 8.76],
                [7.97, 9.12, 5.93, 8.09],
                [9.03, 8.97, 8.19, 8.10],
                [7.41, 7.87, 6.77, 7.23],
            ]
        )
        self.weights = {0: 9.00, 1: 8.24, 2: 5.98, 3: 8.48}
        self.preference = {0: 0.50, 1: 0.50, 2: 0.50, 3: 0.50}
        self.indifference = {0: 0.30, 1: 0.30, 2: 0.30, 3: 0.30}
        self.veto = {0: 0.70, 1: 0.70, 2: 0.70, 3: 0.70}
        self.electre = Electre3(
            self.weights,
            self.preference,
            self.indifference,
            self.veto,
            0.3,
            -0.15,
        )

    def test_constructor(self):
        self.assertEqual(self.electre.criteria_weights, self.weights)
        self.assertEqual(self.electre.preference_thresholds, self.preference)
        self.assertEqual(
            self.electre.indifference_thresholds, self.indifference
        )
        self.assertEqual(self.electre.veto_thresholds, self.veto)
        self.assertEqual(self.electre.alpha, 0.3)
        self.assertEqual(self.electre.beta, -0.15)
        other = Electre3(
            self.weights, self.preference, self.indifference, self.veto
        )
        self.assertIsNotNone(other.alpha)
        self.assertIsNotNone(other.beta)

    def test_concordance(self):
        concordance_matrix = DataFrame(
            [
                [1.0, 1.0, 0.73, 0.69, 0.54, 0.96],
                [0.81, 1.0, 0.73, 0.32, 0.11, 0.78],
                [0.27, 0.46, 1.0, 0.55, 0.27, 0.81],
                [0.53, 0.72, 0.73, 1.0, 0.53, 0.81],
                [1.0, 1.0, 0.73, 1.0, 1.0, 1.0],
                [0.46, 0.46, 0.66, 0.19, 0.0, 1.0],
            ]
        )
        # Absolute value = 0.006 according to usual math rounding method
        # (if last digit >5 => round to superior else otherwise
        assert_frame_equal(
            self.electre.concordance(self.table),
            concordance_matrix,
            atol=0.006,
        )
        self.assertRaises(
            ValueError,
            Electre3(
                self.weights,
                self.preference,
                {0: 1.30, 1: 1.30, 2: 1.30, 3: 1.30},
                self.veto,
            ).concordance,
            self.table,
        )

    def test_discordance(self):
        discordance_mat = [
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 0, 0],
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0.5499999999999973, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
            ],
            [
                [1, 1, 1, 0],
                [1, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 0.4499999999999994, 0],
                [1, 1, 1, 0],
                [0, 0, 1, 0],
            ],
            [
                [1, 0, 0, 0],
                [0.5000000000000028, 0, 0, 0],
                [0, 0, 0, 0.8499999999999999],
                [0, 0, 0, 0],
                [1, 0, 1, 0],
                [0, 0, 1, 0],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0.8000000000000009],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
            [
                [1, 1, 0, 0],
                [1, 0.6999999999999985, 0, 0],
                [0, 0, 0, 1],
                [0.2999999999999981, 1, 0, 1],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ],
        ]
        discordance_mat = DataFrame(
            [
                [Series({i: x for i, x in enumerate(aaa)}) for aaa in aa]
                for aa in discordance_mat
            ]
        )

        # Absolute value = 0.006 according to usual math rounding method
        # (if last digit >5 => round to superior else otherwise
        assert_frame_equal(
            self.electre.discordance(self.table), discordance_mat, atol=0.006
        )
        self.assertRaises(
            ValueError,
            Electre3(
                self.weights,
                self.preference,
                self.preference,
                {0: 0.20, 1: 0.20, 2: 0.20, 3: 0.20},
            ).discordance,
            self.table,
        )

    def test_construct(self):
        credibility_mat = DataFrame(
            [
                [1, 1, 0, 0, 0, 0.96227129],
                [0, 1, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1, 0.0, 0.0, 0.0],
                [0.0, 0.71608833, 0.41073113, 1, 0.0, 0.0],
                [1.0, 1.0, 0.54764151, 1.0, 1, 1.0],
                [0.0, 0, 0.0, 0.0, 0.0, 1],
            ]
        )

        assert_frame_equal(
            self.electre.construct(self.table), credibility_mat, atol=0.006
        )

        credibility_mat = DataFrame(
            [
                [1.0, 1.0, 0.73, 0.69, 0.54, 0.96],
                [0.81, 1.0, 0.73, 0.32, 0.11, 0.78],
                [0.27, 0.46, 1.0, 0.55, 0.27, 0.81],
                [0.53, 0.72, 0.73, 1.0, 0.53, 0.81],
                [1.0, 1.0, 0.73, 1.0, 1.0, 1.0],
                [0.46, 0.46, 0.66, 0.19, 0.0, 1.0],
            ]
        )
        assert_frame_equal(
            Electre3(
                self.weights,
                self.preference,
                self.indifference,
                {0: None, 1: None, 2: None, 3: None, 4: None},
            ).construct(self.table),
            credibility_mat,
            atol=0.006,
        )

    def test_qualification(self):
        qualification_list = Series(
            {0: 1.0, 1: -2.0, 2: 0.0, 3: -1.0, 4: 4.0, 5: -2.0}
        )
        assert_series_equal(
            self.electre.qualification(self.electre.construct(self.table)),
            qualification_list,
            atol=0.006,
            check_dtype=False,
        )

    def test_distillation(self):
        desc_distillate = [[4], [0], [1, 2, 3, 5]]
        asc_distillate = [[2, 4], [0, 3], [1, 5]]
        self.assertEqual(
            self.electre.distillation(self.electre.construct(self.table)),
            desc_distillate,
        )
        self.assertEqual(
            self.electre.distillation(
                self.electre.construct(self.table), ascending=True
            ),
            asc_distillate,
        )

    def test_call(self):
        ranking = OutrankingMatrix(
            [
                [1, 1, 0, 1, 0, 1],
                [0, 1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0, 1],
                [0, 1, 0, 1, 0, 1],
                [1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 0, 1],
            ]
        )
        self.assertEqual(self.electre(self.table), ranking)


class TestElectreTri(unittest.TestCase):
    def setUp(self):
        self.scales = {
            0: QuantitativeScale(0, 1),
            1: QuantitativeScale(3, 4),
            2: QuantitativeScale(1, 2),
            3: QuantitativeScale(0, 1),
            4: QuantitativeScale(30, 100),
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
            self.scales,
        )
        self.weights = {0: 30, 1: 30, 2: 20, 3: 10, 4: 10}
        self.preference = {0: 0.05, 1: 0.1, 2: 0.05, 3: 0.1, 4: 8}
        self.indifference = {0: 0.02, 1: 0.05, 2: 0.02, 3: 0.05, 4: 2}
        self.veto = {0: 0.15, 1: 0.6, 2: 0.25, 3: 0.25, 4: 15}
        self.category_profiles = PerformanceTable(
            [
                [0.750, 3.500, 1.300, 0.730, 42.00],
                [0.800, 3.700, 1.370, 0.790, 43.000],
            ]
        )
        self.lambda_ = 0.7
        self.electre = ElectreTri(
            self.weights,
            self.category_profiles,
            self.preference,
            self.indifference,
            self.veto,
            self.lambda_,
        )

    def test_constructor(self):
        self.assertEqual(
            self.electre.category_profiles, self.category_profiles
        )
        self.assertEqual(self.electre.criteria_weights, self.weights)
        self.assertEqual(self.electre.preference_thresholds, self.preference)
        self.assertEqual(
            self.electre.indifference_thresholds, self.indifference
        )
        self.assertEqual(self.electre.veto_thresholds, self.veto)

    def test_concordance(self):
        assert_frame_equal(
            Electre3(
                self.weights, self.preference, self.indifference, self.veto
            ).concordance(self.table),
            self.electre.concordance(self.table),
        )

    def test_discordance(self):
        assert_frame_equal(
            Electre3(
                self.weights, self.preference, self.indifference, self.veto
            ).discordance(self.table),
            self.electre.discordance(self.table),
        )

    def test_construct(self):
        credibility_matrix = DataFrame(
            [
                [
                    1.0,
                    0.03254788396077838,
                    0.0,
                    0.07259259259259267,
                    0.8333333333333335,
                    0.13333333333333333,
                    0.8818333333333334,
                    0.0,
                    0.8000000000000002,
                    0.14820415879017004,
                ],
                [
                    0.9003333333333333,
                    1.0,
                    0.8,
                    0.9371666666666667,
                    1.0,
                    0.8321666666666667,
                    0.82,
                    0.0,
                    0.9393333333333334,
                    0.9226666666666666,
                ],
                [
                    1.0,
                    0.24857142857142864,
                    1.0,
                    0.5,
                    1.0,
                    0.5,
                    1.0,
                    0.0,
                    1.0,
                    0.6799999999999988,
                ],
                [
                    0.9965,
                    0.7,
                    0.8230000000000001,
                    1.0,
                    1.0,
                    0.9,
                    0.845,
                    0.0,
                    1.0,
                    0.9599999999999999,
                ],
                [
                    0.9108333333333333,
                    0.10000000000000009,
                    0.5600000000000014,
                    0.24766666666666673,
                    1.0,
                    0.34266666666666673,
                    0.8,
                    0.0,
                    0.9498333333333333,
                    0.31316666666666654,
                ],
                [
                    0.9000000000000001,
                    0.2666666666666664,
                    0.628,
                    0.7,
                    0.7,
                    1.0,
                    0.95,
                    0.0,
                    0.7,
                    0.7,
                ],
                [
                    0.5,
                    0.0,
                    0.1003866745984533,
                    0.03062499999999996,
                    0.29142857142857137,
                    0.2239999999999998,
                    1.0,
                    0.0,
                    0.4,
                    0.05624999999999985,
                ],
                [
                    0.2999999999999994,
                    0.0,
                    0.07241379310344849,
                    0.0,
                    0.14999999999999925,
                    0.0,
                    0.8,
                    1.0,
                    0.49999999999999956,
                    0.14999999999999925,
                ],
                [
                    0.801,
                    0.06000000000000013,
                    0.2834355828220857,
                    0.333333333333334,
                    0.8,
                    0.3333333333333338,
                    0.8428333333333333,
                    0.0,
                    1.0,
                    0.17560975609756074,
                ],
                [1.0, 0.5, 0.8375, 0.8, 1.0, 0.8, 0.9595, 0.0, 1.0, 1.0],
            ]
        )

        assert_frame_equal(
            credibility_matrix,
            self.electre.construct(self.table),
        )

    def test_call(self):
        exp_optimistic_classes = {
            0: [6],
            1: [0, 2, 4],
            2: [1, 3, 5],
            -1: [7],
        }
        exp_pessimistic_classes = {
            0: [0, 4, 6],
            1: [2, 3, 5],
            2: [1],
            -1: [7],
        }
        optimistic_classes, pessimistic_classes = self.electre(self.table)
        self.assertEqual(optimistic_classes, exp_optimistic_classes)
        self.assertEqual(pessimistic_classes, exp_pessimistic_classes)

        extreme_profil = PerformanceTable(
            [
                [0.650, 3.00, 1.200, 0.70, 42.00],
                [0.850, 4.00, 1.50, 0.90, 50.000],
            ]
        )

        extreme_dataset = PerformanceTable(
            [
                [0.720, 3.560, 1.340, 0.62, 44.340],
                [0.760, 3.630, 1.380, 0.89, 48.750],
                [0.780, 3.740, 1.450, 0.72, 42.130],
                [0.740, 3.540, 1.370, 0.73, 36.990],
                [0.690, 3.740, 1.450, 0.84, 42.430],
                [0.7, 3.280, 1.280, 0.83, 47.430],
            ],
            self.scales,
        )
        other = ElectreTri(
            self.weights,
            extreme_profil,
            self.preference,
            self.indifference,
            self.veto,
            self.lambda_,
        )
        exp_optimistic_classes = {
            1: [0, 1, 2, 3, 4, 5],
        }
        exp_pessimistic_classes = {
            1: [0, 1, 2, 3, 4, 5],
        }
        optimistic_classes, pessimistic_classes = other(extreme_dataset)
        self.assertEqual(optimistic_classes, exp_optimistic_classes)
        self.assertEqual(pessimistic_classes, exp_pessimistic_classes)
