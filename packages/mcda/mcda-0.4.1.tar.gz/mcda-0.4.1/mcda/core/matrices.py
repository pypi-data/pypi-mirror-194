"""This module contains all functions related to matrices.
"""
from itertools import product
from typing import List, Set

from graphviz import Digraph
from pandas import DataFrame
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, floyd_warshall

from mcda.core.set_functions import HashableSet


def dataframe_equals(df1: DataFrame, df2: DataFrame) -> bool:
    """Check if two dataframes have the same values.

    It will realign the indexes and columns if they are ordered differently.

    :param df1:
    :param df2:
    :return:

    .. todo:: integrate into :class:`mcda/core.adjacency_matrix.Matrix`
    """
    return df1.to_dict() == df2.to_dict()


class Matrix:
    """This class implements a wrapper on :class:`pandas.DataFrame`.

    It adds a method to check if two such objects are equals.
    It is meant to be use for any class that needs a DataFrame as its
    internal data representation in this package.

    :param df: dataframe containing the matrix

    :attribute df: dataframe containing the matrix
    """

    def __init__(self, data):
        self.df = DataFrame(data)

    def __mul__(self, other: "Matrix") -> "Matrix":
        """Return element-wise product.

        :param other:
        :return:
        """
        return self.__class__(self.df * other.df)

    def __eq__(self, other) -> bool:
        """Check if both matrices have the same dataframe

        :return:

        .. note:: vertices order does not matter
        """
        if type(other) != type(self):
            return False
        return dataframe_equals(self.df, other.df)


class AdjacencyMatrix(Matrix):
    """This class implements graphs as an adjacency matrix.

    The adjacency matrix is represented internally by a
    :class:`pandas.DataFrame` with vertices as the indexes and columns.

    :param data: adjacency matrix in an array-like or dict-structure
    :param vertices:

    :attribute df: dataframe containing the adjacency matrix
    """

    def __init__(self, data, vertices: List = None):
        df = DataFrame(data, index=vertices, columns=vertices)
        if df.columns.tolist() != df.index.tolist():
            raise ValueError(
                f"{self.__class__} supports only same labelled"
                "index and columns"
            )
        super().__init__(df)

    @property
    def vertices(self) -> List:
        """Return list of vertices"""
        return self.df.index.tolist()

    def plot(
        self, edge_label: bool = False, self_loop: bool = False
    ) -> Digraph:
        """Create a graph for adjacency matrix.

        This function creates a Graph using graphviz and display it.

        :param edge_label: (optional) parameter to display the value of edges
        :param self_loop: (optional) parameter to display self looping edges
        """
        graph = Digraph("graph", strict=True)
        graph.attr("node", shape="box")

        for v in self.vertices:
            graph.node(str(v))
        for a in self.vertices:
            for b in self.vertices:
                if not self_loop and a == b:
                    continue
                if self.df.loc[self.df.index == a, self.df.columns == b].all(
                    None
                ):
                    graph.edge(
                        str(a),
                        str(b),
                        label=str(
                            self.df.loc[
                                self.df.index == a, self.df.columns == b
                            ]
                        )
                        if edge_label
                        else "",
                    )
        graph.render()
        return graph


class BinaryAdjacencyMatrix(AdjacencyMatrix):
    """This class implements graphs as a binary adjacency matrix.

    The adjacency matrix is represented internally by a
    :class:`pandas.DataFrame` with vertices as the indexes and columns.

    :param data: adjacency matrix in an array-like or dict-structure
    :param vertices:

    :attribute df: dataframe containing the adjacency matrix

    :raise ValueError: if non-binary values are in the matrix
    """

    def __init__(self, data, vertices: List = None):
        super().__init__(data, vertices)
        if ((self.df != 1) & (self.df != 0)).any(axis=None):
            raise ValueError(
                "AdjacencyMatrix objects must contain binary values"
            )

    @property
    def transitive_closure(self) -> "BinaryAdjacencyMatrix":
        """Return transitive closure of matrix"""
        _m = floyd_warshall(csr_matrix(self.df.to_numpy())) < float("inf")
        m = DataFrame(
            _m,
            index=self.vertices,
            columns=self.vertices,
        )
        res = DataFrame(
            0,
            index=self.vertices,
            columns=self.vertices,
        )
        res[m] = 1
        return self.__class__(res)

    @property
    def transitive_reduction(self) -> "BinaryAdjacencyMatrix":
        """Return transitive reduction of matrix.

        .. note:: this function can change the matrix shape
        """
        matrix = self.graph_condensation
        path_matrix = floyd_warshall(csr_matrix(matrix.df.to_numpy())) == 1
        nodes = range(len(matrix.df))
        for u in nodes:
            for v in nodes:
                if path_matrix[u][v]:
                    for w in nodes:
                        if path_matrix[v][w]:
                            matrix.df.iloc[u, w] = 0
        return matrix

    @property
    def graph_condensation(self) -> "BinaryAdjacencyMatrix":
        """Return the condensation graph

        .. note:: the matrix output by this function is acyclic

        .. warning:: this function changes the matrix shape
        """

        n_components, labels = connected_components(
            self.df.to_numpy(), connection="strong"
        )
        # Return input matrix if no cycle found
        if n_components == len(self.df):
            return self.__class__(self.df)
        # Create new matrix with appropriate names for components
        components = []
        for component_index in range(n_components):
            component = HashableSet(
                self.df.index[labels == component_index].tolist()
            )
            components.append(component)
        new_matrix = DataFrame(0, index=components, columns=components)
        for component_a, component_b in product(
            range(n_components), range(n_components)
        ):
            if component_a != component_b:
                new_matrix.iloc[component_a, component_b] = (
                    self.df.iloc[labels == component_a, labels == component_b]
                    .to_numpy()
                    .any()
                )

        return self.__class__(new_matrix.astype(int))

    @property
    def cycle_reduction_matrix(self) -> "BinaryAdjacencyMatrix":
        """Return matrix with cycles removed."""
        n_components, labels = connected_components(
            self.df.to_numpy(), connection="strong"
        )
        components = range(n_components)
        new_matrix = DataFrame(0, index=self.vertices, columns=self.vertices)
        for component_a, component_b in product(components, components):
            if component_a != component_b:
                new_matrix.loc[
                    labels == component_a, labels == component_b
                ] = (
                    self.df.loc[labels == component_a, labels == component_b]
                    .to_numpy()
                    .any()
                )
        return self.__class__(new_matrix.astype(int))

    @property
    def kernel(self) -> List:
        """Return the kernel of the graph if existing.

        The kernel is a *stable* and *dominant* set of nodes.
        Dominant nodes are the origin of edges, dominated ones are the target.

        :return: the kernel (if existing), else an empty list
        """
        graph = self.df.copy()
        # We remove self loops
        for v in self.vertices:
            graph.at[v, v] = 0
        kernel: Set = set()
        outsiders: Set = set()
        while not graph.empty:
            domination = (graph == 0).all(axis=0)
            dominators = domination[domination].index.tolist()
            if len(dominators) == 0:
                return []

            dominated = (graph == 1).loc[dominators].any(axis=0)
            neighbours = dominated[dominated].index.tolist()

            to_remove = dominators + neighbours
            graph = graph.drop(index=to_remove, columns=to_remove)
            kernel = kernel.union(dominators)
            outsiders = outsiders.union(neighbours)
        return list(kernel)
