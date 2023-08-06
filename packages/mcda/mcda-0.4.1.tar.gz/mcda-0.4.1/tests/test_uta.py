import unittest

from pulp import LpMinimize, LpProblem

from mcda.core.performance_table import PerformanceTable
from mcda.core.relations import (
    IncomparableRelation,
    IndifferenceRelation,
    PreferenceRelation,
    PreferenceStructure,
)
from mcda.core.scales import PreferenceDirection, QuantitativeScale
from mcda.mavt.uta import UTA, UTAstar


class UTATestCase(unittest.TestCase):
    def setUp(self):
        self.alternatives = [
            "Peugeot 505 GR",
            "Opel Record 2000 LS",
            "Citroen Visa Super E",
            "VW Golf 1300 GLS",
            "Citroen CX 2400 Pallas",
            "Mercedes 230",
            "BMW 520",
            "Volvo 244 DL",
            "Peugeot 104 ZS",
            "Citroen Dyane",
        ]
        self.scales = {
            0: QuantitativeScale(110, 190),
            1: QuantitativeScale(7, 15, PreferenceDirection.MIN),
            2: QuantitativeScale(6, 13, PreferenceDirection.MIN),
            3: QuantitativeScale(3, 13),
            4: QuantitativeScale(5, 9),
            5: QuantitativeScale(20000, 80000, PreferenceDirection.MIN),
        }
        self.performance_table = PerformanceTable(
            [
                [173, 11.4, 10.01, 10, 7.88, 49500],
                [176, 12.3, 10.48, 11, 7.96, 46700],
                [142, 8.2, 7.3, 5, 5.65, 32100],
                [148, 10.5, 9.61, 7, 6.15, 39150],
                [178, 14.5, 11.05, 13, 8.06, 64700],
                [180, 13.6, 10.4, 13, 8.47, 75700],
                [182, 12.7, 12.26, 11, 7.81, 68593],
                [145, 14.3, 12.95, 11, 8.38, 55000],
                [161, 8.6, 8.42, 7, 5.11, 35200],
                [117, 7.2, 6.75, 3, 5.81, 24800],
            ],
            alternatives=self.alternatives,
            scales=self.scales,
        )
        self.criteria_segments = {0: 5, 1: 4, 2: 4, 3: 5, 4: 4, 5: 5}
        self.relations = PreferenceStructure()
        for i in range(len(self.alternatives) - 1):
            self.relations += PreferenceRelation(
                self.alternatives[i], self.alternatives[i + 1]
            )
        self.normalized_table = self.performance_table.normalize()
        self.u_var = UTA._generate_marginal_utility_variables(
            self.criteria_segments
        )
        self.g_matrix = UTA._generate_criteria_values_matrix(
            self.criteria_segments
        )
        self.sigma_var = UTA._generate_alternatives_errors_variables(
            self.alternatives
        )
        self.uta = UTA(
            self.performance_table,
            self.relations,
            self.criteria_segments,
            delta=0.01,
        )

    def test_constructor(self):
        self.assertEqual(self.uta.performance_table, self.performance_table)
        self.assertEqual(self.uta.relations, self.relations)
        self.assertEqual(self.uta.delta, 0.01)
        self.assertIsNotNone(self.uta.post_optimality_problem)
        self.assertIsNotNone(self.uta.problem)
        self.assertEqual(self.uta.problem.sense, LpMinimize)

        uta = UTA(self.performance_table, self.relations)
        self.assertEqual(
            uta.criteria_segments,
            {c: 2 for c in self.performance_table.criteria},
        )

        relations = self.relations.copy()
        del relations[self.alternatives[0], self.alternatives[1]]
        relations += IncomparableRelation(
            self.alternatives[0], self.alternatives[1]
        )
        self.assertRaises(TypeError, UTA, self.performance_table, relations)

    def test_generate_criteria_values_matrix(self):
        self.assertEqual(len(self.g_matrix), len(self.criteria_segments))
        for i in self.g_matrix.keys():
            self.assertEqual(
                len(self.g_matrix[i]), self.criteria_segments[i] + 1
            )

    def test_generate_marginal_utility_variables(self):
        self.assertEqual(len(self.u_var), len(self.criteria_segments))
        for i in self.u_var.keys():
            self.assertEqual(len(self.u_var[i]), self.criteria_segments[i] + 1)

    def test_generate_alternatives_errors_variables(self):
        self.assertEqual(len(self.sigma_var), len(self.alternatives))
        var = UTA._generate_alternatives_errors_variables(
            self.alternatives, "prefix"
        )
        for i, a in enumerate(self.alternatives):
            self.assertEqual(var[a].name, f"prefix_{i}")

    def test_generate_utility_variable(self):
        self.assertIsNotNone(
            UTA._generate_utility_variable(
                self.normalized_table.get_alternative_values_at(0),
                self.u_var,
                self.g_matrix,
            )
        )
        self.assertIsNotNone(
            UTA._generate_utility_variable(
                self.performance_table.get_alternative_values_at(0),
                self.u_var,
                self.g_matrix,
            )
        )

    def test_add_uta_constraints(self):
        prob = LpProblem("UTA", LpMinimize)
        self.assertIsNone(prob.objective)
        relations = self.relations.copy()
        del relations[self.alternatives[2], self.alternatives[3]]
        relations += IndifferenceRelation(
            self.alternatives[2],
            self.alternatives[3],
        )
        UTA._add_uta_constraints(
            prob,
            self.normalized_table,
            self.u_var,
            self.sigma_var,
            self.g_matrix,
            relations,
        )
        self.assertEqual(
            len(prob.constraints),
            len(relations) + sum(len(u_i) for u_i in self.u_var.values()) + 1,
        )

    def test_disaggregate(self):
        functions = self.uta.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertEqual(self.uta.objective, 0)

        uta = UTA(
            self.performance_table,
            self.relations,
            self.criteria_segments,
            delta=0.01,
            post_optimality=True,
        )
        functions = uta.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertAlmostEqual(uta.objective, 0)

        relations = self.relations.copy()
        del relations[self.alternatives[2], self.alternatives[3]]
        relations += IndifferenceRelation(
            self.alternatives[2],
            self.alternatives[3],
        )
        uta = UTA(
            self.performance_table,
            relations,
            self.criteria_segments,
            delta=0.01,
            post_optimality=True,
        )
        functions = uta.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertAlmostEqual(uta.objective, 0)


class UTAstarTestCase(unittest.TestCase):
    def setUp(self):
        self.alternatives = [
            "Peugeot 505 GR",
            "Opel Record 2000 LS",
            "Citroen Visa Super E",
            "VW Golf 1300 GLS",
            "Citroen CX 2400 Pallas",
            "Mercedes 230",
            "BMW 520",
            "Volvo 244 DL",
            "Peugeot 104 ZS",
            "Citroen Dyane",
        ]
        self.scales = {
            0: QuantitativeScale(110, 190),
            1: QuantitativeScale(7, 15, PreferenceDirection.MIN),
            2: QuantitativeScale(6, 13, PreferenceDirection.MIN),
            3: QuantitativeScale(3, 13),
            4: QuantitativeScale(5, 9),
            5: QuantitativeScale(20000, 80000, PreferenceDirection.MIN),
        }
        self.performance_table = PerformanceTable(
            [
                [173, 11.4, 10.01, 10, 7.88, 49500],
                [176, 12.3, 10.48, 11, 7.96, 46700],
                [142, 8.2, 7.3, 5, 5.65, 32100],
                [148, 10.5, 9.61, 7, 6.15, 39150],
                [178, 14.5, 11.05, 13, 8.06, 64700],
                [180, 13.6, 10.4, 13, 8.47, 75700],
                [182, 12.7, 12.26, 11, 7.81, 68593],
                [145, 14.3, 12.95, 11, 8.38, 55000],
                [161, 8.6, 8.42, 7, 5.11, 35200],
                [117, 7.2, 6.75, 3, 5.81, 24800],
            ],
            alternatives=self.alternatives,
            scales=self.scales,
        )
        self.criteria_segments = {0: 5, 1: 4, 2: 4, 3: 5, 4: 4, 5: 5}
        self.relations = PreferenceStructure()
        for i in range(len(self.alternatives) - 1):
            self.relations += PreferenceRelation(
                self.alternatives[i], self.alternatives[i + 1]
            )
        self.normalized_table = self.performance_table.normalize()
        self.w_var = UTA._generate_marginal_utility_variables(
            self.criteria_segments
        )
        self.g_matrix = UTA._generate_criteria_values_matrix(
            self.criteria_segments
        )
        self.uta_star = UTAstar(
            self.performance_table,
            self.relations,
            self.criteria_segments,
            delta=0.01,
        )

    def test_generate_utility_variable_star(self):
        self.assertIsNotNone(
            UTAstar._generate_utility_variable_star(
                self.performance_table.get_alternative_values_at(0),
                self.w_var,
                self.g_matrix,
            )
        )

    def test_add_uta_star_constraints(self):
        prob = LpProblem("UTA_star", LpMinimize)
        self.assertIsNone(prob.objective)
        sigma_p_var = UTAstar._generate_alternatives_errors_variables(
            self.alternatives, "sigma_p"
        )
        sigma_n_var = UTAstar._generate_alternatives_errors_variables(
            self.alternatives, "sigma_n"
        )
        relations = self.relations.copy()
        del relations[self.alternatives[2], self.alternatives[3]]
        relations += IndifferenceRelation(
            self.alternatives[2],
            self.alternatives[3],
        )
        UTAstar._add_uta_star_constraints(
            prob,
            self.normalized_table,
            self.w_var,
            sigma_p_var,
            sigma_n_var,
            self.g_matrix,
            relations,
        )
        self.assertEqual(
            len(prob.constraints),
            len(relations) + 1,
        )

    def test_constructor(self):
        self.assertEqual(self.uta_star.problem.sense, LpMinimize)
        self.assertIsNotNone(self.uta_star.post_optimality_problem)

    def test_disaggregate(self):
        functions = self.uta_star.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertEqual(self.uta_star.objective, 0)

        uta_star = UTAstar(
            self.performance_table,
            self.relations,
            self.criteria_segments,
            delta=0.01,
            post_optimality=True,
        )
        functions = uta_star.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertAlmostEqual(uta_star.objective, 0)

        relations = self.relations.copy()
        del relations[self.alternatives[2], self.alternatives[3]]
        relations += IndifferenceRelation(
            self.alternatives[2],
            self.alternatives[3],
        )
        uta_star = UTAstar(
            self.performance_table,
            relations,
            self.criteria_segments,
            delta=0.01,
            post_optimality=True,
        )
        functions = uta_star.disaggregate()
        grades = functions(self.performance_table)
        ranks = grades.sort_values(ascending=False)
        self.assertEqual(grades.index.tolist(), ranks.index.tolist())
        self.assertAlmostEqual(uta_star.objective, 0)
