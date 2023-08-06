from abc import ABC
from inspect import isclass
from typing import Any, Dict, Iterator, List, Tuple, Union, cast

from graphviz import Digraph
from numpy import fill_diagonal
from pandas import DataFrame, Series

from mcda.core.matrices import BinaryAdjacencyMatrix

from .performance_table import Scores
from .scales import PreferenceDirection


class Relation(ABC):
    """This class represents a pairwise relation between two elements.

    :param a: first element
    :param b: second element

    :attribute a:
    :attribute b:
    :attribute DRAW_STYLE: (class) key args for plotting all instances
    """

    _RELATION_TYPE = ""
    DRAW_STYLE: Dict[str, Any] = {"style": "invis"}

    def __init__(self, a: Any, b: Any):
        self.a = a
        self.b = b
        self.validate()

    def __repr__(self) -> str:
        """Return representation of object.

        :return:
        """
        return f"{self.a} {self._RELATION_TYPE} {self.b}"

    @property
    def elements(self) -> Tuple[Any, Any]:
        """Return elements of the relation"""
        return self.a, self.b

    def validate(self):
        """Check whether a relation is valid or not."""
        pass

    def same_elements(self, relation: "Relation") -> bool:
        """Check whether the relations are about the same pair of alternatives.

        :param relation: second relation
        :return:
            ``True`` if both relations share the same elements pair, ``False``
            otherwise

        .. warning:: Does not check for relations' validity!
        """
        return set(self.elements) == set(relation.elements)

    def __eq__(self, other: Any) -> bool:
        """Check whether relations are equal.

        :param other:
        :return: check result

        .. warning:: Does not check for relations' validity!
        """
        if type(other) == type(self):
            return self.elements == other.elements
        return False

    def __add__(self, other: "Relation") -> "PreferenceStructure":
        """Build new preference structure as addition of both relations.

        :return: relations added to new preference structure
        """
        if not isinstance(other, Relation):
            raise TypeError("can only add one other Relation object")
        return PreferenceStructure([self, other])

    def __hash__(self) -> int:
        """Hash object based on its unordered list of elements"""
        return hash(self.a) + hash(self.b)

    def compatible(self, other: "Relation") -> bool:
        """Check whether both relations can coexist in the same preference
        structure.

        Relations are compatible if equal or having different elements pair.

        :param other:
        :return: check result

        .. warning:: Does not check for relations' validity!
        """
        return self == other or not self.same_elements(other)

    @classmethod
    def types(cls) -> List:
        """Return list of relation types.

        :return:
        """
        return cls.__subclasses__()

    def _draw(self, graph: Digraph):
        """Draw relation on provided graph"""
        graph.edge(str(self.a), str(self.b), **self.DRAW_STYLE)


class PreferenceRelation(Relation):
    """This class represents a preference relation between two elements.

    A relation is read `aPb`.

    :param a: first element
    :param b: second element

    :attribute a:
    :attribute b:
    :attribute DRAW_STYLE: (class) key args for plotting all instances

    .. note:: this relation is antisymmetric and irreflexive
    """

    _RELATION_TYPE = "P"
    DRAW_STYLE: Dict[str, Any] = {}

    def validate(self):
        """Check whether a relation is valid or not.

        :raise ValueError: if relation is reflexive
        """
        if self.a == self.b:
            raise ValueError(
                f"Preference relations are irreflexive: {self.a} == {self.b}"
            )


class IndifferenceRelation(Relation):
    """This class represents an indifference relation between two elements.

    A relation is read `aIb`.

    :param a: first element
    :param b: second element

    :attribute a:
    :attribute b:
    :attribute DRAW_STYLE: (class) key args for plotting all instances

    .. note:: this relation is symmetric and reflexive
    """

    _RELATION_TYPE = "I"
    DRAW_STYLE = {"arrowhead": "none"}

    __hash__ = Relation.__hash__

    def __eq__(self, other):
        """Check whether relations are equal.

        :param other:
        :return: check result

        .. warning:: Does not check for relations' validity!
        """
        if type(other) == type(self):
            return self.same_elements(other)
        return False


class IncomparableRelation(Relation):
    """This class represents an incomparable relation between two elements.

    A relation is read `aRb`.

    :param a: first element
    :param b: second element

    :attribute a:
    :attribute b:
    :attribute DRAW_STYLE: (class) key args for plotting all instances

    .. note:: this relation is symmetric and irreflexive
    """

    _RELATION_TYPE = "R"
    DRAW_STYLE = {"arrowhead": "none", "style": "dotted"}

    __hash__ = Relation.__hash__

    def __eq__(self, other):
        """Check whether relations are equal.

        :param other:
        :return: check result

        .. warning:: Does not check for relations' validity!
        """
        if type(other) == type(self):
            return self.same_elements(other)
        return False

    def validate(self):
        """Check whether a relation is valid or not.

        :raise ValueError: if relation is reflexive
        """
        if self.a == self.b:
            raise ValueError(
                f"Incomparable relations are irreflexive: {self.a} == {self.b}"
            )


class PreferenceStructure:
    """This class represents a list of relations.

    :param data:
    """

    def __init__(
        self,
        data: Union[List[Relation], Relation, "PreferenceStructure"] = None,
    ):
        data = [] if data is None else data
        if isinstance(data, Relation):
            relations = [data]
        elif isinstance(data, PreferenceStructure):
            relations = data.relations
        else:
            relations = data
        self._relations = list(set(relations))
        self.validate()

    @property
    def elements(self) -> List[Any]:
        """Return elements present in relations list."""
        return list(set(e for r in self._relations for e in r.elements))

    @property
    def relations(self) -> List[Relation]:
        """Return copy of relations list."""
        return self._relations.copy()

    def validate(self):
        """Check whether the relations are all valid.

        :raise ValueError: if at least two relations are incompatible
        """
        for i, r1 in enumerate(self._relations):
            for r2 in self._relations[(i + 1) :]:
                if not r1.compatible(r2):
                    raise ValueError(f"incompatible relations: {r1}, {r2}")

    @property
    def is_total_preorder(self) -> bool:
        """Check whether relations list is a total preorder or not"""
        return (
            len(
                PreferenceStructure(
                    self.transitive_closure[IncomparableRelation]
                )
            )
            == 0
        )

    @property
    def is_total_order(self) -> bool:
        """Check whether relations list is a total order or not"""
        res = self.transitive_closure
        return (
            len(PreferenceStructure(res[IncomparableRelation]))
            + len(PreferenceStructure(res[IndifferenceRelation]))
            == 0
        )

    def __eq__(self, other: Any):
        """Check if preference structure is equal to another.

        Equality is defined as having the same set of relations.

        :return:

        .. note:: `other` type is not coerced
        """
        if isinstance(other, PreferenceStructure):
            return set(other.relations) == set(self._relations)
        return False

    def __len__(self) -> int:
        """Return number of relations in the preference structure.

        :return:
        """
        return len(self._relations)

    def __repr__(self) -> str:
        """Return representation of relations contained in structure

        :return:
        """
        return self._relations.__repr__()

    def _relation(
        self,
        *args: Any,
    ) -> Union[Relation, "PreferenceStructure", None]:
        """Return all relations between given elements of given types.

        If no relation type is supplied, all are considered.
        If no element is supplied, all are considered.

        :param *args:
        :return:

        .. warning:: Does not check for a relation's validity or redundancy!
        """
        elements = []
        types = []
        for arg in args:
            if isclass(arg) and issubclass(arg, Relation):
                types.append(arg)
            else:
                elements.append(arg)
        elements = self.elements if len(elements) == 0 else elements
        types = Relation.types() if len(types) == 0 else types
        res = None
        for r in self._relations:
            if r.a in elements and r.b in elements and r.__class__ in types:
                res = r if res is None else cast(Relation, res) + r
        return res

    def _element_relations(
        self, a: Any
    ) -> Union[Relation, "PreferenceStructure", None]:
        """Return all relations involving given element.

        :param a: element
        :return:

        .. warning:: Does not check for a relation's validity or redundancy!
        """
        res = None
        for r in self._relations:
            if a in r.elements:
                res = r if res is None else cast(Relation, res) + r
        return res

    def __getitem__(
        self, item: Any
    ) -> Union[Relation, "PreferenceStructure", None]:
        """Return all relations matching the request

        :param item:
        :return:
            Depending on `item` type:
                * pair of elements: search first relation with this elements
                pair
                * element: all relations involving element
                * relation class: all relations of this class
        """
        if isinstance(item, tuple):
            return self._relation(*item)
        if isclass(item):
            return self._relation(item)
        return self._element_relations(item)

    def __delitem__(self, item: Any):
        """Remove all relations matching the request

        :param item:
        :return:
            Depending on `item` type:
                * pair of elements: search first relation with this elements
                pair
                * element: all relations involving element
                * relation class: all relations of this class
        """
        r = self[item]
        to_delete = PreferenceStructure(r)._relations
        self._relations = [rr for rr in self._relations if rr not in to_delete]

    def __contains__(self, item: Any) -> bool:
        """Check whether a relation is already in the preference structure.

        :param item: relation
        :return: check result

        .. warning:: Does not check for a relation's validity!
        """
        for r in self._relations:
            if r == item:
                return True
        return False

    def __add__(self, other: Any) -> "PreferenceStructure":
        """Create new preference structure with appended relations.

        :param other:
            * :class:`Relation`: relation is appended into new object
            * :class:`PreferenceStructure`: all relations are appended into new
            object
        :return:
        """
        if hasattr(other, "__iter__"):
            return self.__class__(self._relations + [r for r in other])
        return self.__class__(self._relations + [other])

    def __iter__(self) -> Iterator[Relation]:
        """Return iterator over relations

        :return:
        """
        return iter(self._relations)

    @property
    def transitive_closure(self) -> "PreferenceStructure":
        """Apply transitive closure to preference structure and return result.

        .. warning:: Does not check for a valid preference structure!
        """
        return self.from_outranking_matrix(
            cast(OutrankingMatrix, self.outranking_matrix.transitive_closure)
        )

    @property
    def transitive_reduction(self) -> "PreferenceStructure":
        """Apply transitive reduction to preference structure and return result

        .. warning:: Does not check for a valid preference structure!

        .. warning:: This function may bundle together multiple elements
        """
        return self.from_outranking_matrix(
            cast(OutrankingMatrix, self.outranking_matrix.transitive_reduction)
        )

    @property
    def outranking_matrix(self) -> "OutrankingMatrix":
        """Return corresponding outranking matrix."""
        elements = self.elements
        matrix = DataFrame(0, index=elements, columns=elements)
        fill_diagonal(matrix.values, 1)
        for r in self._relations:
            a, b = r.elements
            if isinstance(r, PreferenceRelation):
                matrix.loc[matrix.index == a, matrix.columns == b] = 1
            if isinstance(r, IndifferenceRelation):
                matrix.loc[matrix.index == a, matrix.columns == b] = 1
                matrix.loc[matrix.index == b, matrix.columns == a] = 1
        return OutrankingMatrix(matrix)

    @classmethod
    def from_outranking_matrix(
        cls, matrix: "OutrankingMatrix"
    ) -> "PreferenceStructure":
        """Transform an outranking matrix to a preference structure.

        :param matrix: the matrix of relations
        :return: preference structure
        """
        relations: List[Relation] = list()
        for ii, i in enumerate(matrix.vertices):
            for j in matrix.vertices[ii + 1 :]:
                if matrix.df.loc[
                    matrix.df.index == i, matrix.df.columns == j
                ].all(None):
                    if matrix.df.loc[
                        matrix.df.index == j, matrix.df.columns == i
                    ].all(None):
                        relations.append(IndifferenceRelation(i, j))
                    else:
                        relations.append(PreferenceRelation(i, j))
                elif matrix.df.loc[
                    matrix.df.index == j, matrix.df.columns == i
                ].all(None):
                    relations.append(PreferenceRelation(j, i))
                else:
                    relations.append(IncomparableRelation(i, j))
        return cls(relations)

    @classmethod
    def from_scores(cls, scores: Scores) -> "PreferenceStructure":
        """Convert scores into preference structure.

        :param scores: alternatives' score
        :return:

        .. note::
            The minimum number of relations representing the scores is returned
            (w.r.t transitivity of preference and indifference relations)
        """
        res: List[Relation] = []
        sorted_scores = scores.sort()
        for a, b in zip(sorted_scores.labels[:-1], sorted_scores.labels[1:]):
            if sorted_scores[a] == sorted_scores[b]:
                res.append(IndifferenceRelation(a, b))
            else:
                res.append(PreferenceRelation(a, b))
        return cls(res)

    def plot(self, relation_types: List = None) -> Digraph:
        """Create a graph for list of relation.

        This function creates a Graph using graphviz and display it.
        """
        relation_types = (
            [PreferenceRelation, IndifferenceRelation]
            if relation_types is None
            else relation_types
        )
        relation_graph = Digraph("relations", strict=True)
        relation_graph.attr("node", shape="box")
        for e in self.elements:
            relation_graph.node(str(e))
        for r in self._relations:
            for c in relation_types:
                if isinstance(r, c):
                    r._draw(relation_graph)
                    continue
        relation_graph.render()
        return relation_graph

    def copy(self) -> "PreferenceStructure":
        """Copy preference structure into new object.

        :return: copy
        """
        return PreferenceStructure(self)


class OutrankingMatrix(BinaryAdjacencyMatrix):
    """This class implements an outranking matrix as an adjacency matrix.

    The outranking matrix is represented internally by a
    :class:`pandas.DataFrame` with vertices as the indexes and columns.

    :param data: adjacency matrix in an array-like or dict-structure
    :param vertices:

    :attribute df: dataframe containing the adjacency matrix
    """

    @property
    def preference_structure(self) -> PreferenceStructure:
        """Return corresponding preference structure."""
        return PreferenceStructure.from_outranking_matrix(self)

    @classmethod
    def from_preference_structure(
        cls, preference_structure: PreferenceStructure
    ) -> "OutrankingMatrix":
        """Transform a preference structure into an outranking matrix.

        :param preference_structure: the matrix of relations
        :return: outranking matrix
        """
        return preference_structure.outranking_matrix

    @classmethod
    def from_ranked_categories(cls, categories: List[List[Any]]):
        """Convert a ranking of categories of alternatives into an outranking
        matrix.

        :param categories:
            the ranked categories (each category is a list of alternatives)
        :return: outranking matrix
        """

        alternatives = [a for ll in categories for a in ll]
        res = cls(0, vertices=alternatives)
        for category in categories:
            res.df.loc[category, category] = 1
            res.df.loc[
                category, alternatives[alternatives.index(category[-1]) + 1 :]
            ] = 1
        return res


class Ranking(Scores):
    """This class describes a ranking as a :class:`Scores`.

    It is intended as a shorthand to create rankings.

    :param data:

    :attr data: internal representation of data
    :attr scales:
        scales of the data (one per value, all equals to the same
        :class:`mcda.core.scales.QuantitativeScale` with bounds inferred from
        data and minimize preference direction)
    """

    def __init__(self, data: Series):
        super().__init__(
            data=data, preference_direction=PreferenceDirection.MIN
        )

    def copy(self) -> "Ranking":
        """Return a copy of the object"""
        return Ranking(self.data.copy())
