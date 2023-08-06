import unittest

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from mcda.core.matrices import (
    AdjacencyMatrix,
    BinaryAdjacencyMatrix,
    Matrix,
    dataframe_equals,
)
from mcda.core.set_functions import HashableSet


def test_dataframe_equals():
    df1 = DataFrame([[0, 1], [1, 1]], index=["a", "b"], columns=["c", "d"])
    df2 = DataFrame([[0, 1], [1, 1]], index=["a", "b"], columns=["c", "d"])
    df3 = DataFrame([[1, 1], [0, 1]], index=["b", "a"], columns=["c", "d"])
    df4 = DataFrame([[1, 0], [1, 1]], index=["a", "b"], columns=["d", "c"])
    df5 = DataFrame([[1, 1], [1, 0]], index=["b", "a"], columns=["d", "c"])
    df6 = DataFrame([[0, 1], [1, 1]], index=["aa", "b"], columns=["c", "d"])
    df7 = DataFrame([[0, 1], [1, 1]], index=["a", "b"], columns=["cc", "d"])
    assert dataframe_equals(df1, df2)
    assert dataframe_equals(df1, df3)
    assert dataframe_equals(df1, df4)
    assert dataframe_equals(df1, df5)
    assert not dataframe_equals(df1, df6)
    assert not dataframe_equals(df1, df7)


class MatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.df = DataFrame(
            [[0, 1, 2], [3, 4, 5]],
            index=["a", "b"],
            columns=["aa", "bb", "cc"],
        )
        self.matrix = Matrix(self.df)

    def test_constructor(self):
        assert_frame_equal(self.matrix.df, self.df)

    def test_multiply(self):
        b = Matrix(DataFrame(2, index=self.df.index, columns=self.df.columns))
        assert_frame_equal((self.matrix * b).df, 2 * self.df)

    def test_equal(self):
        self.assertEqual(
            Matrix(
                DataFrame(
                    self.df.values.tolist(),
                    index=self.df.index.tolist(),
                    columns=self.df.columns.tolist(),
                )
            ),
            self.matrix,
        )
        self.assertNotEqual(
            Matrix(
                DataFrame(
                    self.df.values.tolist(),
                )
            ),
            self.matrix,
        )
        self.assertNotEqual(
            self.matrix,
            DataFrame(
                self.df.values.tolist(),
                index=self.df.index.tolist(),
                columns=self.df.columns.tolist(),
            ),
        )


class XMatrixTestCase(unittest.TestCase):
    def setUp(self):
        self.vertices = ["a", "b", "c"]
        self.df = DataFrame([[0, 0.5, 1], [-1.2, 2.5, 0], [0.1, 0.2, 0.3]])
        self.matrix = AdjacencyMatrix(self.df, self.vertices)

    def test_constructor(self):
        assert_frame_equal(
            self.matrix.df,
            DataFrame(self.df, index=self.vertices, columns=self.vertices),
        )
        self.assertEqual(self.matrix.vertices, self.vertices)
        self.assertEqual(
            AdjacencyMatrix(self.df).vertices, [*range(len(self.df))]
        )
        self.assertRaises(
            ValueError,
            AdjacencyMatrix,
            DataFrame([[0]], index=["a"], columns=["b"]),
        )


class AdjacencyMatrixTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.vertices = ["a", "b", "c", "d", "e"]
        self.matrix = BinaryAdjacencyMatrix(
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ],
            self.vertices,
        )
        self.reordered_matrix = BinaryAdjacencyMatrix(
            [
                [1, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ],
            ["a", "c", "b", "d", "e"],
        )
        self.table = [
            [1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
        ]
        self.transitive_closure = BinaryAdjacencyMatrix(
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
            ],
            self.vertices,
        )
        self.transitive_reduction = BinaryAdjacencyMatrix(
            [[0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [
                HashableSet(("a",)),
                HashableSet(("b", "c")),
                HashableSet(("d",)),
                HashableSet(("e",)),
            ],
        )
        self.graph_condensation = BinaryAdjacencyMatrix(
            [[0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [
                HashableSet(("a",)),
                HashableSet(("b", "c")),
                HashableSet(("d",)),
                HashableSet(("e",)),
            ],
        )

    def test_constructor(self):
        assert_frame_equal(
            self.matrix.df,
            DataFrame(self.table, index=self.vertices, columns=self.vertices),
        )
        assert_frame_equal(
            BinaryAdjacencyMatrix(self.table).df, DataFrame(self.table)
        )
        self.assertRaises(ValueError, BinaryAdjacencyMatrix, DataFrame([0.2]))

    def test_equal(self):
        self.assertEqual(
            self.matrix,
            BinaryAdjacencyMatrix(self.table, self.vertices),
        )
        self.assertNotEqual(self.matrix, self.table)
        self.assertEqual(self.matrix, self.reordered_matrix)

    def test_vertices(self):
        self.assertEqual(self.matrix.vertices, self.vertices)
        self.assertEqual(
            BinaryAdjacencyMatrix(self.table).vertices,
            [*range(len(self.table))],
        )

    def test_graph_condensation(self):
        self.assertEqual(
            self.matrix.graph_condensation, self.graph_condensation
        )
        matrix = BinaryAdjacencyMatrix(
            DataFrame([[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]])
        )
        self.assertEqual(matrix.graph_condensation, matrix)

    def test_transitive_reduction(self):
        self.assertEqual(
            self.matrix.transitive_reduction, self.transitive_reduction
        )
        matrix = BinaryAdjacencyMatrix(
            DataFrame([[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]])
        )
        expected_matrix = BinaryAdjacencyMatrix(
            DataFrame([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
        )
        self.assertEqual(matrix.transitive_reduction, expected_matrix)

    def test_transitive_closure(self):
        self.assertEqual(
            self.matrix.transitive_closure, self.transitive_closure
        )

    def test_cycle_reduction(self):
        matrix = BinaryAdjacencyMatrix(
            [
                [1, 1, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 0],
                [0, 1, 0, 1, 1, 0],
                [0, 0, 0, 1, 1, 0],
                [0, 0, 0, 1, 0, 1],
                [0, 0, 0, 1, 0, 0],
            ]
        )
        expected_matrix = BinaryAdjacencyMatrix(
            [
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(matrix.cycle_reduction_matrix, expected_matrix)

    def test_kernel(self):
        self.assertEqual(self.matrix.kernel, [])
        self.assertEqual(
            set(self.matrix.cycle_reduction_matrix.kernel), {"b", "c", "e"}
        )
