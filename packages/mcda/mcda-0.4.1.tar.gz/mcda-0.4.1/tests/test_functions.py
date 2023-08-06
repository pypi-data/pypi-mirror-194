import pytest

from mcda.core.functions import (
    AffineFunction,
    DiscreteFunction,
    FuzzyNumber,
    Interval,
    PieceWiseFunction,
)


def test_intervals():
    # Test constructor
    i = Interval(0, 1)
    assert i.dmin == 0 and i.dmax == 1
    assert i.min_in and i.max_in
    with pytest.raises(Exception) as e:
        Interval(2, 1)
    assert e.type == ValueError

    # Check is empty
    assert Interval(0, 0, False).is_empty()
    assert not Interval(0, 0).is_empty()

    # Check inside
    assert 0 in i and 1 in i and not i.inside(1.1)
    i = Interval(0, 1, False, False)
    assert 0 not in i and 1 not in i
    assert 0 not in Interval(0, 0, False)

    # Check normalize
    i = Interval(1, 2)
    assert i.normalize(1) == 0 and i.normalize(2) == 1

    # Check denormalize
    assert i.denormalize(0) == 1 and i.denormalize(1) == 2

    # Check intersection
    i = Interval(-10, 10)
    res = i.intersect(Interval(-5, 15))
    assert res.dmin == -5 and res.dmax == 10 and res.min_in and res.max_in
    res = i.intersect(Interval(-20, 20))
    assert res.dmin == -10 and res.dmax == 10 and res.min_in and res.max_in
    res = i.intersect(Interval(-5, 5, False))
    assert res.dmin == -5 and res.dmax == 5 and not res.min_in and res.max_in
    assert i.intersect(Interval(-50, -20, False, False)).is_empty()
    assert i.intersect(Interval(-50, -10, False, False)).is_empty()

    # Check join
    i = Interval(-10, 10, False)
    res = i.join(Interval(-5, 15))
    assert res.dmin == -10 and res.dmax == 15 and not res.min_in and res.max_in
    res = i.join(Interval(-20, 20))
    assert res.dmin == -20 and res.dmax == 20 and res.min_in and res.max_in
    res = i.join(Interval(-5, 5, False))
    assert res.dmin == -10 and res.dmax == 10 and not res.min_in and res.max_in

    # Check union
    i = Interval(-10, 10, True, False)
    res = i.union(Interval(-20, -10))
    assert res.dmin == -20 and res.dmax == 10 and res.min_in and not res.max_in
    res = i.union(Interval(-5, 15))
    assert res.dmin == -10 and res.dmax == 15 and res.min_in and res.max_in
    res = i.union(Interval(-20, 20))
    assert res.dmin == -20 and res.dmax == 20 and res.min_in and res.max_in
    res = i.union(Interval(-5, 5, False))
    assert res.dmin == -10 and res.dmax == 10 and res.min_in and not res.max_in
    assert i.union(Interval(20, 30)).is_empty()
    assert i.union(Interval(10, 30)).is_empty()
    i = Interval(-10, 10)
    res = i.join(Interval(10, 20))
    assert res.dmin == -10 and res.dmax == 20

    # Check continuous
    i = Interval(-10, 10, True, False)
    assert i.continuous(Interval(10, 20, True))
    assert not i.continuous(Interval(10, 20, False))
    assert not i.continuous(Interval(15, 20, True))
    assert not i.continuous(Interval(-20, -10, False))

    # Check relation operators
    i = Interval(-10, 10, False, False)
    assert i == Interval(-10, 10, False, False)
    assert i != Interval(-10, 10, True)


def test_affine_function_from_segments():
    # Test valid affine function creation
    f = AffineFunction(1, 0.5)
    assert f(0) == 0.5 and f(1) == 1.5

    segment = [[0, 0], [1, 2]]
    f = AffineFunction(segment=segment)
    assert f(0) == 0 and f(1) == 2

    # Test error cases
    with pytest.raises(Exception) as ex:
        AffineFunction(segment=[[0, 0]])
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        AffineFunction(segment=[[0, 0], []])
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        AffineFunction(segment=[[], [0, 0]])
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        AffineFunction(segment=[[0, 1], [0, 0]])
    assert ex.type == ValueError


def test_discrete_functions():
    # Test constructor
    values = {"a": 1, "b": 2, "c": 3}
    f = DiscreteFunction(values)
    assert len(f.values) == 3
    assert f("a") == 1 and f("b") == 2 and f("c") == 3

    with pytest.raises(Exception) as ex:
        f("d")
    assert ex.type == IndexError


def test_piecewise_functions():
    # Test constructor
    intervals = [Interval(0, 2.5, max_in=False), Interval(2.5, 5)]
    functions = [
        lambda x: x,
        lambda x: -0.5 * x + 2.0,
    ]
    f = PieceWiseFunction(intervals, functions)
    assert f(0) == 0 and f(2.5) == 0.75
    assert len(f.intervals) == len(f.functions)
    with pytest.raises(Exception) as ex:
        PieceWiseFunction(intervals, [])
    assert ex.type == ValueError
    f = PieceWiseFunction(
        segments=[[[0, 0], [2.5, 1, False]], [[2.5, 2], [5, 1.5]]]
    )
    assert len(f.functions) == 2

    # Test apply
    assert f(2.5) == 2 and f(5) == 1.5 and f(0) == 0 and f(1.25) == 0.5
    with pytest.raises(Exception) as ex:
        f(-500)
    assert ex.type == ValueError

    # Test continuity
    assert not f.continuous()
    f = PieceWiseFunction(intervals, [lambda x: 5, lambda x: 2 * x])
    assert f.continuous()
    f.intervals[1].min_in = False
    assert not f.continuous()
    f = PieceWiseFunction([Interval(0, 1)], [lambda x: 2 * x + 3.5])
    f(0.5)
    assert f.continuous()


def test_fuzzy_numbers():
    # Test constructor
    f = FuzzyNumber([0, 2.5, 2.5, 5])
    assert f.average == 2.5
    f2 = FuzzyNumber([1, 1, 1, 1])
    assert len(f2.intervals) == 1
    assert f2.intervals[0].dmin == f2.intervals[0].dmax
    assert f2(1) == 1
    assert f2(150) == 0
    with pytest.raises(Exception) as ex:
        FuzzyNumber([])
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        FuzzyNumber([0, 1, 2, 1.5])
    assert ex.type == ValueError
    assert f.centre_of_gravity == 2.5
    assert f2.centre_of_gravity == 1
    assert f.centre_of_maximum == 2.5
    assert f.area == 2.5
    assert f != f.centre_of_gravity
    assert f != f2
    assert f == FuzzyNumber(f.abscissa.copy())
