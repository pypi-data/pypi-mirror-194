import pytest
from pandas import Series

from mcda.core.functions import FuzzyNumber
from mcda.core.scales import (
    FuzzyScale,
    NominalScale,
    PreferenceDirection,
    QualitativeScale,
    QuantitativeScale,
    is_better,
    is_better_or_equal,
)


def test_nominal_scales():
    # Test constructor
    s = NominalScale(["bad", "medium", "good"])
    assert len(s.labels) == 3

    # Test equal
    assert s != ""
    assert s != NominalScale(["bad", "yolo", "good"])
    assert s == NominalScale(s.labels.copy())

    # Test contains
    assert "good" in s and "medium" in s and "bad" in s
    assert "yolo" not in s

    # Test transform_to
    s2 = NominalScale(["bad", "hahaha", "good"])
    assert s.transform_to("good", s2) == "good"
    with pytest.raises(Exception) as ex:
        s.transform_to("medium", s2)
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        s.transform_to("a", s2)
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        s.transform_to("medium")
    assert ex.type == ValueError
    s2 = QuantitativeScale(0, 1)
    with pytest.raises(Exception) as ex:
        s.transform_to("medium", s2)
    assert ex.type == TypeError
    s2 = QualitativeScale(Series({"bad": 1, "medium": 2, "good": 3}))
    assert s.transform_to("good", s2) == "good"

    # Test normalize
    with pytest.raises(Exception) as ex:
        s.normalize("bad")
    assert ex.type == TypeError

    # Test denormalize
    with pytest.raises(Exception) as ex:
        s.denormalize(0)
    assert ex.type == TypeError

    # Test range
    assert len(s.labels) == len(s.range()) == len(s.range(10))
    assert s.labels == s.range()


def test_quantitative_scales():
    # Test constructor
    s = QuantitativeScale(0, 10)
    assert s.dmin == 0 and s.dmax == 10
    assert s.preference_direction == PreferenceDirection.MAX
    with pytest.raises(Exception) as ex:
        QuantitativeScale(0, 10, 10)
    assert ex.type == ValueError

    # Test equal
    assert s != NominalScale(["bad", "yolo", "good"])
    assert s != QuantitativeScale(0, 10, PreferenceDirection.MIN)
    assert s != QuantitativeScale(-1, 10, PreferenceDirection.MAX)
    assert s == QuantitativeScale(0, 10, PreferenceDirection.MAX)

    # Test contains
    assert 0 in s and 1.5 in s and 10 in s
    assert -1 not in s

    # Test normalize_value
    s = QuantitativeScale(0, 10)
    assert s._normalize_value(10) == 1 and s._normalize_value(3) == 0.3
    s = QuantitativeScale(0, 10, PreferenceDirection.MIN)
    assert s._normalize_value(10) == 0 and s._normalize_value(3) == 0.7

    # Test denormalize_value
    s = QuantitativeScale(0, 10)
    assert s._denormalize_value(1) == 10 and s._denormalize_value(0.3) == 3
    s = QuantitativeScale(0, 10, PreferenceDirection.MIN)
    assert s._denormalize_value(1) == 0 and s._denormalize_value(0.3) == 7

    # Test transform_to
    s2 = QuantitativeScale(0, 1, PreferenceDirection.MIN)
    assert s.transform_to(0, s2) == 0 and s.transform_to(10, s2) == 1
    with pytest.raises(Exception) as ex:
        s.transform_to(0)
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        s.transform_to(-5, s2)
    assert ex.type == ValueError
    s2 = NominalScale(["bad"])
    with pytest.raises(Exception) as ex:
        s.transform_to(0, s2)
    assert ex.type == TypeError
    s2 = QualitativeScale(Series({"bad": 1, "medium": 2, "good": 3}))
    assert s.transform_to(0, s2) == "good" and s.transform_to(10, s2) == "bad"

    # Test normalize
    assert s.normalize(10) == 0

    # Test denormalize
    assert s.denormalize(0) == 10

    # Test range
    r = s.range()
    assert len(r) == 2 and r[0] == s.dmin and r[1] == s.dmax
    r = s.range(10)
    assert len(r) == 10

    # Test is_better
    assert s.is_better(0, 1)
    s.preference_direction = PreferenceDirection.MAX
    assert s.is_better(1, 0)

    # Test normal scale
    assert QuantitativeScale.normal() == QuantitativeScale(
        0, 1, PreferenceDirection.MAX
    )


def test_qualitative_scales():
    # Test constructor
    s = QualitativeScale(
        Series({"bad": 3, "medium": 2, "good": 1}), PreferenceDirection.MIN
    )
    assert len(s.labels) == 3
    assert s.preference_direction == PreferenceDirection.MIN
    with pytest.raises(Exception) as ex:
        QualitativeScale(Series({"bad": "3", "medium": 2, "good": 1}))
    assert ex.type == TypeError
    s3 = QualitativeScale(
        Series({"bad": 3, "medium": 2, "good": 1}),
        PreferenceDirection.MIN,
        0,
        5,
    )
    assert 4 in s3.quantitative
    with pytest.raises(Exception) as ex:
        QualitativeScale(Series([1, 2]), dmin=-1, dmax=1)
    assert ex.type == ValueError

    # Test equal
    assert s != QuantitativeScale.normal()
    assert s != s3
    assert s != QualitativeScale(
        Series({"bad": 3, "yolo": 2, "good": 1}), PreferenceDirection.MIN
    )
    assert s != QualitativeScale(
        Series({"bad": 3, "medium": 1, "good": 2}), PreferenceDirection.MIN
    )
    assert s == QualitativeScale(
        Series({"bad": 3, "good": 1, "medium": 2}), PreferenceDirection.MIN
    )

    # Test contains
    assert "good" in s
    assert "yolo" not in s

    # Test transform_to
    assert s.transform_to("bad") == 3
    with pytest.raises(Exception) as e:
        s.transform_to("yolo")
    assert e.type is ValueError
    s2 = NominalScale(["bad", "medium", "good"])
    assert s.transform_to("good", s2) == "good"

    # Test transform_from
    assert s.label_from_value(3) == "bad"
    with pytest.raises(Exception) as e:
        s.label_from_value(0)
    assert e.type is ValueError

    # Test range
    assert len(s.labels) == len(s.range()) == len(s.range(10))
    assert s.labels == s.range()

    # Test is_better
    assert s.is_better("good", "bad")


def test_fuzzy_scales():
    # Test fuzzy scale
    f1 = FuzzyNumber([0, 0, 0.2, 0.3])
    f2 = FuzzyNumber([0.2, 0.4, 0.6, 0.8])
    f3 = FuzzyNumber([0.7, 0.7, 1, 1])
    s = FuzzyScale(Series({"bad": f1, "medium": f2, "good": f3}))
    assert s.dmin == 0 and s.dmax == 1
    assert s.transform_to("bad") == f1.centre_of_gravity
    with pytest.raises(Exception) as ex:
        FuzzyScale(Series({"bad": 3, "medium": 2, "good": 1}))
    assert ex.type == TypeError

    # Test equality
    assert s != QualitativeScale(s.values.copy())
    assert s != FuzzyScale(
        Series(
            {
                "bad": FuzzyNumber([0, 0, 0.2, 0.3]),
                "medium": FuzzyNumber([0.4, 0.6, 0.6, 0.8]),
                "good": FuzzyNumber([0.7, 0.7, 1, 1]),
            }
        ),
    )
    assert s != FuzzyScale(
        Series(
            {
                "bad": FuzzyNumber([0, 0, 0.2, 0.3]),
                "medium": FuzzyNumber([0.2, 0.5, 0.5, 0.8]),
                "good": FuzzyNumber([0.7, 0.7, 1, 1]),
            }
        ),
    )
    assert s == FuzzyScale(
        Series(
            {
                "bad": FuzzyNumber([0, 0, 0.2, 0.3]),
                "medium": FuzzyNumber([0.2, 0.4, 0.6, 0.8]),
                "good": FuzzyNumber([0.7, 0.7, 1, 1]),
            }
        ),
    )

    values = s.defuzzify("centre_of_maximum")
    for k in s.labels:
        assert values[k] == s.fuzzy[k].centre_of_maximum
    s = FuzzyScale(
        Series({"bad": f1, "medium": f2, "good": f3}), dmin=0, dmax=1.5
    )
    assert 1.2 in s.quantitative
    with pytest.raises(Exception) as ex:
        FuzzyScale(
            Series({"bad": f1, "medium": f2, "good": f3}), dmin=-1, dmax=0.5
        )
    assert ex.type == ValueError

    # Test similarity measure
    s = FuzzyScale(Series({"good": f3, "bad": f1, "medium": f2}))
    assert s.similarity(f1, f1) == 1
    fa = FuzzyNumber([0] * 4)
    fb = FuzzyNumber([1] * 4)
    assert s.similarity(fa, fb) == 0

    # Test fuzzy partitions
    assert not s.is_fuzzy_partition()
    s = FuzzyScale(
        Series(
            {
                "Bad": FuzzyNumber([0.0, 0.0, 0.0, 2.0]),
                "Medium": FuzzyNumber([0.0, 2.0, 2.0, 5.0]),
                "Good": FuzzyNumber([2.0, 5.0, 5.0, 6.0]),
            }
        )
    )
    assert s.is_fuzzy_partition()

    # Test ordinal distance
    s = FuzzyScale(Series({"good": f3, "bad": f1, "medium": f2}))
    assert s.ordinal_distance("bad", "bad") == 0
    assert s.ordinal_distance("good", "medium") == 1
    with pytest.raises(Exception) as ex:
        s.ordinal_distance("god", "bad")
    assert ex.type == ValueError
    with pytest.raises(Exception) as ex:
        s.ordinal_distance("good", "worst")
    assert ex.type == ValueError

    # Test fuzziness
    assert s.fuzziness(FuzzyNumber([0.5, 0.5, 0.5, 0.5])) == 0
    assert s.fuzziness(FuzzyNumber([0, 0.5, 0.5, 1])) == 0.5

    # Test specificity
    assert s.specificity(FuzzyNumber([1, 1, 1, 1])) == 1
    assert s.specificity(FuzzyNumber([0, 0.5, 0.5, 1])) == 0.5
    assert s.specificity(FuzzyNumber([0, 0, 1, 1])) == 0


def test_is_better():
    s = QualitativeScale(
        Series({"bad": 3, "medium": 2, "good": 1}), PreferenceDirection.MIN
    )
    assert is_better("good", "medium", s)


def test_is_better_or_equal():
    s = QualitativeScale(
        Series({"bad": 3, "medium": 2, "good": 1}), PreferenceDirection.MIN
    )
    assert is_better_or_equal("good", "medium", s)
    assert is_better_or_equal("good", "good", s)
