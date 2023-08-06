"""This module implements the UTA algorithms.

Implementation and naming conventions are taken from :cite:p:`siskos2005uta`.

.. todo::
    Rework internal methods/functions to make classes prettier and more
    efficient
"""
from typing import Any, Dict, List, cast

import numpy as np
from pandas import Series
from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum
from pulp import value as pulp_value

from mcda.core.performance_table import PerformanceTable, ScaleValues
from mcda.core.relations import (
    IncomparableRelation,
    PreferenceRelation,
    PreferenceStructure,
)

from ..core.aliases import NumericFunction
from ..core.functions import PieceWiseFunction
from ..core.interfaces import Trainer
from .aggregators import UtilityFunction


class UTA(Trainer[UtilityFunction]):
    """This class represents the UTA disaggregator.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver

    :raise TypeError:
        if `relations` contains a
        :class:`mcda.api.core.relations.IncomparableRelation` instance

    :attribute problem: UTA base LP problem
    :attribute post_optimality_problem: UTA post optimal LP problem

    .. note::
        Post-optimality threshold is computed as follows:
        (1 + `post_optimality_coeff`) * F_star
        where F_star is the optimum objective cost computed by UTA

    .. note::
        `criteria_functions` are computed for normal scales, so when
        applying aggregation you must provide normalized values (
        :class:`mcda.api.core.PerformanceTable` alone are automatically
        normalized)
    """

    def __init__(
        self,
        performance_table: PerformanceTable,
        relations: PreferenceStructure,
        criteria_segments: Dict[Any, int] = None,
        delta: float = 0.001,
        post_optimality: bool = False,
        post_optimality_coeff: float = 0,
        solver_args: dict = None,
    ):
        if relations[IncomparableRelation] is not None:
            raise TypeError(
                f"{self.__class__} does not support IncomparableRelation "
                "structures"
            )
        self.performance_table = performance_table
        self.relations = relations
        self.criteria_segments = (
            {criterion: 2 for criterion in performance_table.criteria}
            if criteria_segments is None
            else criteria_segments
        )
        self.delta = delta
        self.post_optimality = post_optimality
        self.post_optimality_coeff = post_optimality_coeff
        self.solver_args = {} if solver_args is None else solver_args

        # Create LP Problem
        self.problem = LpProblem("UTA", LpMinimize)
        self.post_optimality_problem = LpProblem("Post-Optimality", LpMinimize)

    @property
    def objective(self):
        """Return objective function final value.

        Objective taken from base `problem` or `post_optimality_problem`.
        """
        if self.post_optimality:
            return pulp_value(self.post_optimality_problem.objective)
        return pulp_value(self.problem.objective)

    def disaggregate(self) -> UtilityFunction:
        """Perform disaggregation and return result.

        :return: utility functions
        """
        return self.train()

    def train(self) -> UtilityFunction:
        """Perform disaggregation using UTA and return result.

        :return: utility functions
        """
        # Create all UTA variables
        g = self._generate_criteria_values_matrix(self.criteria_segments)
        u_var = self._generate_marginal_utility_variables(
            self.criteria_segments
        )
        sigma_var = self._generate_alternatives_errors_variables(
            self.performance_table.alternatives
        )

        # Create LP Problem
        self.problem = LpProblem("UTA", LpMinimize)

        # Add objective function
        self.problem += lpSum(sigma_var.values())

        # Add constraints
        self._add_uta_constraints(
            self.problem,
            self.performance_table.normalize(),
            u_var,
            sigma_var,
            g,
            self.relations,
            self.delta,
        )

        # Solve problem
        self.problem.solve(**self.solver_args)

        # Compute optimum solution
        u_star = {
            criterion: [u_ij.varValue for u_ij in u_i]
            for criterion, u_i in u_var.items()
        }
        F_star = pulp_value(self.problem.objective)

        if not self.post_optimality:
            # Compute optimum utility functions
            criteria_functions: Dict[Any, NumericFunction] = {}
            for criterion in u_star.keys():
                points = [
                    [g_ij, u_ij]
                    for g_ij, u_ij in zip(g[criterion], u_star[criterion])
                ]
                segments = [
                    [p1, p2] for p1, p2 in zip(points[:-1], points[1:])
                ]
                criteria_functions[criterion] = PieceWiseFunction(
                    segments=segments
                )
            return UtilityFunction(criteria_functions)

        # Compute post-optimal utility functions
        max_cost = F_star * (1 + self.post_optimality_coeff)

        u = {
            criterion: [0.0 for _ in range(n + 1)]
            for criterion, n in self.criteria_segments.items()
        }
        for ci, criterion in enumerate(g.keys()):
            for k, sense in zip(["min", "max"], [LpMinimize, LpMaximize]):
                # Create all UTA variables
                u_var = self._generate_marginal_utility_variables(
                    self.criteria_segments
                )
                sigma_var = self._generate_alternatives_errors_variables(
                    self.performance_table.alternatives
                )

                # Create post-optimality subproblem
                prob = LpProblem(f"post-Optimality-{ci}-{k}", sense)

                # Add objective function
                prob += u_var[criterion][-1]

                # Add post-optimality constraint on UTA objective value
                prob += lpSum(sigma_var.values()) <= max_cost

                # Add regular UTA constraints
                self._add_uta_constraints(
                    prob,
                    self.performance_table.normalize(),
                    u_var,
                    sigma_var,
                    g,
                    self.relations,
                    self.delta,
                )

                # Solve post-optimality subproblem
                prob.solve(**self.solver_args)

                # Add solution to compounded post-optimality solution
                for i, u_i in u_var.items():
                    for j, u_ij in enumerate(u_i):
                        u[i][j] += u_ij.varValue
        # Average solutions
        for i in u:
            for j in range(len(u[i])):
                u[i][j] /= 2 * len(g)

        criteria_functions = {}
        for criterion in g.keys():
            points = [
                [g_ij, u_ij] for g_ij, u_ij in zip(g[criterion], u[criterion])
            ]
            segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
            criteria_functions[criterion] = PieceWiseFunction(
                segments=segments
            )

        # Compute post-optimality cost
        self.post_optimality_problem = LpProblem("Post-Optimality", LpMinimize)
        self.post_optimality_problem += lpSum(sigma_var.values())
        u_a = cast(
            Series,
            self.performance_table.normalize()
            .apply_criteria_functions(criteria_functions)  # type: ignore
            .sum(axis=1),
        )
        for relation in self.relations:
            if isinstance(relation, PreferenceRelation):
                self.post_optimality_problem += (
                    u_a[relation.a]
                    + sigma_var[relation.a]
                    - u_a[relation.b]
                    - sigma_var[relation.b]
                    >= self.delta
                )
            else:
                self.post_optimality_problem += (
                    u_a[relation.a]
                    + sigma_var[relation.a]
                    - u_a[relation.b]
                    - sigma_var[relation.b]
                    == 0
                )
        self.post_optimality_problem.solve(**self.solver_args)

        return UtilityFunction(criteria_functions)

    @staticmethod
    def _generate_criteria_values_matrix(
        criteria_segments: Dict[str, int],
    ) -> Dict[Any, List[float]]:
        """Compute criteria values matrix.

        :param criteria_segments: number of segments per criteria
        :return:
        """
        return {
            criterion: np.linspace(0, 1, nb_segments + 1).tolist()
            for criterion, nb_segments in criteria_segments.items()
        }

    @staticmethod
    def _generate_marginal_utility_variables(
        criteria_segments: Dict[str, int],
    ) -> Dict[Any, List[LpVariable]]:
        """Return initial marginal utility functions variables.

        :param criteria_segments: number of segments per criteria
        :return:
        """
        return {
            criterion: [
                LpVariable(f"u_{i}_{j}", lowBound=0, cat="continuous")
                for j in range(criteria_segments[criterion] + 1)
            ]
            for i, criterion in enumerate(criteria_segments.keys())
        }

    @staticmethod
    def _generate_alternatives_errors_variables(
        alternatives: List[Any], prefix: str = "sigma"
    ) -> Dict[Any, LpVariable]:
        """Return initial alternatives errors variables.

        :param alternatives:
        :param prefix: prefix for :class:`pulp.LpVariable` name
        :return:
        """
        return {
            alternative: LpVariable(
                f"{prefix}_{k}", lowBound=0, cat="continuous"
            )
            for k, alternative in enumerate(alternatives)
        }

    @staticmethod
    def _generate_utility_variable(
        alternative_values: ScaleValues,
        u_var: Dict[Any, List[LpVariable]],
        g_matrix: Dict[Any, List[float]],
    ) -> Any:
        """Generate initial utility variable for a given alternative.

        :param alternative_values: performances of the given alternative
        :param u_var: utility function variables
        :param g_matrix: criteria values matrix
        :return:

        .. note:: Used by UTA algorithm
        """
        u_i_var = []
        for criterion, val in alternative_values.data.items():
            g_i = g_matrix[criterion]
            u_i = u_var[criterion]
            for j, g_ij in enumerate(g_i[1:]):
                if val <= g_ij:
                    u_i_var.append(
                        u_i[j]
                        + (val - g_i[j])
                        * (u_i[j + 1] - u_i[j])
                        / (g_i[j + 1] - g_i[j])
                    )
                    break
        return lpSum(u_i_var)

    @staticmethod
    def _add_uta_constraints(
        problem: LpProblem,
        performance_table: PerformanceTable,
        u_var: Dict[Any, List[LpVariable]],
        sigma_var: Dict[Any, LpVariable],
        g_matrix: Dict[Any, List[float]],
        relations: PreferenceStructure,
        delta: float = 0.001,
    ):
        """Add UTA constraints to LP problem.

        :param problem:
        :param performance_table:
        :param u_var: utility function variables
        :param sigma_var: alternatives errors variables
        :param g_matrix: criteria values matrix
        :param relations: pairwise relations between alternatives
        :param delta: discrimination threshold for preference relations
        :return:
        """
        # Preference constraints
        u_a = {}
        for relation in relations:
            for k in relation.elements:
                if k not in u_a:
                    u_a[k] = UTA._generate_utility_variable(
                        performance_table.get_alternative_values(k),
                        u_var,
                        g_matrix,
                    )
            if isinstance(relation, PreferenceRelation):
                problem += (
                    u_a[relation.a]
                    + sigma_var[relation.a]
                    - u_a[relation.b]
                    - sigma_var[relation.b]
                    >= delta
                )
            else:
                problem += (
                    u_a[relation.a]
                    + sigma_var[relation.a]
                    - u_a[relation.b]
                    - sigma_var[relation.b]
                    == 0
                )

        # Marginal utility monotonicity constraints
        for u_i in u_var.values():
            problem += u_i[0] == 0
            for u_ij, u_ij1 in zip(u_i[:-1], u_i[1:]):
                problem += u_ij1 - u_ij >= 0

        # Utility normalization constraint
        problem += lpSum(u_i[-1] for u_i in u_var.values()) == 1


class UTAstar(UTA):
    """This class represents the UTA\\* disaggregator.

    :param performance_table:
    :param criteria_segments: number of segments per criteria
    :param relations: pairwise relations between alternatives
    :param delta: discrimination threshold for preference relations
    :param post_optimality: if ``True``, post-optimality is applied
    :param post_optimality_coeff:
        coefficient used to compute threshold on UTA objective function cost
        when performing post-optimality
    :param solver_args: extra arguments supplied to the solver

    :raise TypeError:
        if `relations` contains a
        :class:`mcda.api.core.relations.IncomparableRelation` instance

    :attribute problem: UTA\\* base LP problem
    :attribute post_optimality_problem: UTA\\* post optimal LP problem
    :attribute criteria_functions: utility functions as criteria functions

    .. note::
        Post-optimality threshold is computed as follows:
        (1 + `post_optimality_coeff`) * F_star
        where F_star is the optimum objective cost computed by UTA\\*

    .. note::
        `criteria_functions` are computed for normal scales, so when
        applying aggregation you must provide normalized values (
        :class:`mcda.api.core.PerformanceTable` alone are automatically
        normalized)
    """

    def disaggregate(self) -> UtilityFunction:
        """Perform disaggregation using UTA\\* and return result.

        :return: utility functions
        """
        # Create all UTA variables
        g = self._generate_criteria_values_matrix(self.criteria_segments)
        w_var = self._generate_marginal_utility_variables(
            self.criteria_segments
        )
        sigma_p_var = self._generate_alternatives_errors_variables(
            self.performance_table.alternatives, "sigma_p"
        )
        sigma_n_var = self._generate_alternatives_errors_variables(
            self.performance_table.alternatives, "sigma_n"
        )

        # Create LP Problem
        self.problem = LpProblem("UTA_star", LpMinimize)

        # Add objective function
        self.problem += lpSum(sigma_p_var.values()) + lpSum(
            sigma_n_var.values()
        )

        # Add constraints
        self._add_uta_star_constraints(
            self.problem,
            self.performance_table.normalize(),
            w_var,
            sigma_p_var,
            sigma_n_var,
            g,
            self.relations,
            self.delta,
        )

        # Solve problem
        self.problem.solve(**self.solver_args)

        # Compute optimum solution
        w_star = {
            criterion: [w_ij.varValue for w_ij in w_i]
            for criterion, w_i in w_var.items()
        }
        F_star = pulp_value(self.problem.objective)

        if not self.post_optimality:
            # Compute optimum utility functions
            criteria_functions: Dict[Any, NumericFunction] = {}
            for criterion in w_star.keys():
                points = [
                    [g_ij, sum(w_star[criterion][: (j + 1)])]
                    for j, g_ij in enumerate(g[criterion])
                ]
                segments = [
                    [p1, p2] for p1, p2 in zip(points[:-1], points[1:])
                ]
                criteria_functions[criterion] = PieceWiseFunction(
                    segments=segments
                )
            return UtilityFunction(criteria_functions)

        # Compute post-optimal utility functions
        max_cost = F_star * (1 + self.post_optimality_coeff)

        w = {
            criterion: [0.0 for _ in range(n + 1)]
            for criterion, n in self.criteria_segments.items()
        }
        for ci, criterion in enumerate(g.keys()):
            for k, sense in zip(["min", "max"], [LpMinimize, LpMaximize]):
                # Create all UTA* variables
                w_var = self._generate_marginal_utility_variables(
                    self.criteria_segments
                )
                sigma_p_var = self._generate_alternatives_errors_variables(
                    self.performance_table.alternatives, "sigma_p"
                )
                sigma_n_var = self._generate_alternatives_errors_variables(
                    self.performance_table.alternatives, "sigma_n"
                )

                # Create post-optimality subproblem
                prob = LpProblem(f"post-Optimality-{ci}-{k}", sense)

                # Add objective function
                prob += lpSum(w_var[criterion])

                # Add post-optimality constraint on UTA* objective value
                prob += (
                    lpSum(sigma_p_var.values()) + lpSum(sigma_n_var.values())
                    <= max_cost
                )

                # Add regular UTA* constraints
                self._add_uta_star_constraints(
                    prob,
                    self.performance_table.normalize(),
                    w_var,
                    sigma_p_var,
                    sigma_n_var,
                    g,
                    self.relations,
                    self.delta,
                )

                # Solve post-optimality subproblem
                prob.solve(**self.solver_args)

                # Add solution to compounded post-optimality solution
                for i, w_i in w_var.items():
                    for j, w_ij in enumerate(w_i):
                        w[i][j] += w_ij.varValue
        # Average solutions
        for i in w:
            for j in range(len(w[i])):
                w[i][j] /= 2 * len(g)

        # Compute optimum utility functions
        criteria_functions = {}
        for criterion in g.keys():
            points = [
                [g_ij, sum(w[criterion][: (j + 1)])]
                for j, g_ij in enumerate(g[criterion])
            ]
            segments = [[p1, p2] for p1, p2 in zip(points[:-1], points[1:])]
            criteria_functions[criterion] = PieceWiseFunction(
                segments=segments
            )

        # Compute post optimality cost
        self.post_optimality_problem = LpProblem("Post-Optimality", LpMinimize)
        self.post_optimality_problem += lpSum(sigma_p_var.values()) + lpSum(
            sigma_n_var.values()
        )
        u_a = cast(
            Series,
            self.performance_table.normalize()
            .apply_criteria_functions(criteria_functions)  # type: ignore
            .sum(axis=1),
        )
        for relation in self.relations:
            if isinstance(relation, PreferenceRelation):
                self.post_optimality_problem += (
                    u_a[relation.a]
                    + sigma_n_var[relation.a]
                    + sigma_p_var[relation.b]
                    - u_a[relation.b]
                    - sigma_n_var[relation.b]
                    - sigma_p_var[relation.a]
                    >= self.delta
                )
            else:
                self.post_optimality_problem += (
                    u_a[relation.a]
                    + sigma_n_var[relation.a]
                    + sigma_p_var[relation.b]
                    - u_a[relation.b]
                    - sigma_n_var[relation.b]
                    - sigma_p_var[relation.a]
                    == 0
                )
        self.post_optimality_problem.solve(**self.solver_args)

        return UtilityFunction(criteria_functions)

    @staticmethod
    def _generate_utility_variable_star(
        alternative_values: ScaleValues,
        w_var: Dict[Any, List[LpVariable]],
        g_matrix: Dict[Any, List[float]],
    ) -> Any:
        """Generate initial step utility variable for a given alternative.

        `w_var` corresponds to step increases of the utility variables.

        :param alternative_values: performances of the given alternative
        :param w_var: differential utility function variables
        :param g_matrix: criteria values matrix
        :return:
        """
        w_i_var = []
        for criterion, val in alternative_values.data.items():
            g_i = g_matrix[criterion]
            w_i = w_var[criterion]
            prev_g_ij = g_i[0]
            for g_ij, w_ij in zip(g_i, w_i):
                if val >= g_ij:
                    w_i_var.append(w_ij)
                else:
                    w_i_var.append(
                        w_ij * (val - prev_g_ij) / (g_ij - prev_g_ij)
                    )
                    break
                prev_g_ij = g_ij
        return lpSum(w_i_var)

    @staticmethod
    def _add_uta_star_constraints(
        problem: LpProblem,
        performance_table: PerformanceTable,
        w_var: Dict[Any, List[LpVariable]],
        sigma_p_var: Dict[Any, LpVariable],
        sigma_n_var: Dict[Any, LpVariable],
        g_matrix: Dict[Any, List[float]],
        relations: PreferenceStructure,
        delta: float = 0.001,
    ):
        """Add UTA\\* constraints to LP problem.

        :param problem:
        :param performance_table:
        :param w_var: differential utility function variables
        :param sigma_p_var: positive alternatives errors variables
        :param sigma_n_var: negative alternatives errors variables
        :param g_matrix: criteria values matrix
        :param relations: pairwise relations between alternatives
        :param delta: discrimination threshold for preference relations
        :return:
        """

        # Preference constraints
        u_a = {}
        for relation in relations:
            for k in relation.elements:
                if k not in u_a:
                    u_a[k] = UTAstar._generate_utility_variable_star(
                        performance_table.get_alternative_values(k),
                        w_var,
                        g_matrix,
                    )
            if isinstance(relation, PreferenceRelation):
                problem += (
                    u_a[relation.a]
                    + sigma_n_var[relation.a]
                    + sigma_p_var[relation.b]
                    - u_a[relation.b]
                    - sigma_n_var[relation.b]
                    - sigma_p_var[relation.a]
                    >= delta
                )
            else:
                problem += (
                    u_a[relation.a]
                    + sigma_n_var[relation.a]
                    + sigma_p_var[relation.b]
                    - u_a[relation.b]
                    - sigma_n_var[relation.b]
                    - sigma_p_var[relation.a]
                    == 0
                )

        # Normalized utility function
        problem += lpSum(w_ij for w_ij in (w_i for w_i in w_var.values())) == 1
