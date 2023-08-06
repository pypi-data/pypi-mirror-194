import math
from typing import Any, Dict, List, cast

from .aliases import NumericFunction


class AffineFunction:
    """This class defines a callable affine function.

    :param slope:
    :param constant:
    :param segment:
        a list of two points on the affine function line, each point being
        a list with at least abscissa and ordinate

    .. note:: `segment` supersedes `slope` and `constant` if provided

    :attr slope:
    :attr constant:
    """

    def __init__(
        self,
        slope: float = 0,
        constant: float = 0,
        segment: List[List] = None,
    ):
        if segment is None:
            self.slope = slope
            self.constant = constant
        elif len(segment) < 2:
            raise ValueError(
                "two points are needed to define an affine function"
            )
        elif len(segment[0]) < 2 or len(segment[1]) < 2:
            raise ValueError(
                "two coordinates per point are needed to "
                "define an affine function"
            )
        elif segment[0][0] == segment[1][0]:
            raise ValueError(
                "affine function needs two points with different abscissa"
            )
        else:
            self.slope = (segment[0][1] - segment[1][1]) / (
                segment[0][0] - segment[1][0]
            )
            self.constant = (
                segment[1][1] * segment[0][0] - segment[0][1] * segment[1][0]
            ) / (segment[0][0] - segment[1][0])

    def __call__(self, x: float) -> float:
        """Call affine function.

        :param x:
        :return: result
        """
        return self.slope * x + self.constant


class Interval:
    """This class describes a numeric interval.

    :param dmin: min boundary of interval
    :param dmax: max boundary of interval
    :param min_in: is min boundary inside interval or not
    :param max_in: is max boundary inside interval or not
    :raises ValueError: if `dmin` bigger than `dmax`
    """

    def __init__(
        self,
        dmin: float,
        dmax: float,
        min_in: bool = True,
        max_in: bool = True,
    ):
        """Constructor method"""
        if dmin > dmax:
            raise ValueError(
                f"Interval min value '{dmin}' bigger than max value '{dmax}'"
            )
        self.dmin = dmin
        self.dmax = dmax
        self.min_in = min_in
        self.max_in = max_in

    def is_empty(self) -> bool:
        """Check if interval is empty.

        :return: ``True`` if interval is empty, ``False`` otherwise.
        """
        return self.dmin == self.dmax and (not self.min_in or not self.max_in)

    def __contains__(self, x: float) -> bool:
        """Check whether value is inside interval or not.

        :param x:
        :return:
        """
        return self.inside(x)

    def inside(self, x: float) -> bool:
        """Check whether value is inside interval or not.

        :param x:
        :return:
        :rtype: bool
        """
        if self.is_empty():
            return False
        if self.dmin < x < self.dmax:
            return True
        if self.min_in and x == self.dmin:
            return True
        if self.max_in and x == self.dmax:
            return True
        return False

    def normalize(self, x: Any) -> float:
        """Normalize value inside interval.

        :param x:
        :return:
        """
        _x = cast(float, x)
        return (
            (_x - self.dmin) / (self.dmax - self.dmin)
            if self.dmin != self.dmax
            else 0
        )

    def denormalize(self, x: float) -> Any:
        """Denormalize normalized value inside interval.

        :param x:
        :return:
        """
        return x * (self.dmax - self.dmin) + self.dmin

    def join(self, other: "Interval") -> "Interval":
        """Compute maximal junction between two intervals.

        Biggest interval containing both intervals.

        :param other:
        :return:
        """
        dmin = min((self.dmin, other.dmin))
        dmax = max((self.dmax, other.dmax))
        min_in = (self.min_in if dmin == self.dmin else False) or (
            other.min_in if dmin == other.dmin else False
        )
        max_in = (self.max_in if dmax == self.dmax else False) or (
            other.max_in if dmax == other.dmax else False
        )
        return Interval(dmin, dmax, min_in, max_in)

    def intersect(self, other: "Interval") -> "Interval":
        """Compute intersection between two intervals.

        :param other:
        :type other: Interval
        :return:
        :rtype: Interval or None
        """
        dmin = max((self.dmin, other.dmin))
        dmax = min((self.dmax, other.dmax))
        min_in = (self.min_in if dmin == self.dmin else True) and (
            other.min_in if dmin == other.dmin else True
        )
        max_in = (self.max_in if dmax == self.dmax else True) and (
            other.max_in if dmax == other.dmax else True
        )
        if dmin > dmax:
            return Interval(0, 0, False, False)
        return Interval(dmin, dmax, min_in, max_in)

    def union(self, other: "Interval") -> "Interval":
        """Compute union of two intervals.

        :param other:
        :return:

        .. note :: Returns ``None`` if intervals don't coïncide
        """
        if self.intersect(other).is_empty():
            return Interval(0, 0, False, False)
        return self.join(other)

    def continuous(self, other: "Interval") -> bool:
        """Check continuity with following interval.

        :param other:
        :return:

        .. note ::
            Strict continuity is checked (i.e if the intervals touches without
            overlapping).
            In other words : `dmax` equal to `other`'s `dmin`
        """
        if self.dmax != other.dmin:
            return False
        return self.max_in or other.min_in

    def __eq__(self, other: Any) -> bool:
        """Checks both intervals share the same fields.

        :param other:
        :return:
        """
        return (
            self.dmin == other.dmin
            and self.dmax == other.dmax
            and self.min_in == other.min_in
            and self.max_in == other.max_in
        )


class DiscreteFunction:
    """This class implements discrete function.

    :param values: function description, abscissa as keys, ordinates as values
    """

    def __init__(self, values: Dict[Any, Any]):
        """Constructor method"""
        self.values = {}
        self.values.update(values)

    def apply(self, x: Any) -> Any:
        """Apply function to single value.

        :param x:
        :return:
        :raises IndexError: if `x` is not in `values`
        """
        if x not in self.values:
            raise IndexError(f"discrete value '{x}' unknown")
        return self.values[x]

    def __call__(self, x: Any) -> Any:
        """Apply function to single value.

        :param x:
        :return:
        :raises IndexError: if `x` is not in `values`
        """
        return self.apply(x)


class PieceWiseFunction:
    """This class implements piecewise MCDA function.

    :param intervals: functions definition intervals
    :param functions:
    :param segments: list of segments defining piecewise linear functions
    :raises ValueError: if number of intervals and functions are different

    .. note::
        * first matching interval is used to return result
        * each segment of `segments` is a list of two points, each point a
          sequence of numeric abscissa, a numeric ordinate and a :class:`bool`
          indicating if the point is included in the underlying interval
    """

    _TYPE = "PieceWiseFunction"

    def __init__(
        self,
        intervals: List[Interval] = None,
        functions: List[NumericFunction] = None,
        segments: List[List[List]] = None,
    ):
        """Constructor method"""
        intervals = [] if intervals is None else intervals
        functions = [] if functions is None else functions
        segments = [] if segments is None else segments
        if len(intervals) != len(functions):
            raise ValueError(
                f"{self._TYPE} must have as many intervals as functions"
            )
        self.intervals = intervals
        self.functions = functions
        self._parse_segments(segments=segments)

    def _parse_segments(self, segments: List[List[List]]):
        """Parse segments and populate intervals and functions.

        Each segment of `segments` is a list of two points, each point a
        sequence of numeric abscissa, a numeric ordinate and a :class:`bool`
        indicating if the point is included in the underlying interval.

        :param segments:
        """
        for seg in segments:
            a = seg[0] if len(seg[0]) > 2 else seg[0] + [True]
            b = seg[1] if len(seg[1]) > 2 else seg[1] + [True]
            self.intervals.append(Interval(a[0], b[0], a[2], b[2]))
            self.functions.append(AffineFunction(segment=seg))

    def continuous(self) -> bool:
        """Check intervals and functions are ordered and continuous.

        :return:
        """
        if len(self.intervals) <= 1:
            return True
        for i in range(len(self.intervals) - 1):
            if not self.intervals[i].continuous(self.intervals[i + 1]):
                return False
            if not math.isclose(
                self.functions[i](self.intervals[i].dmax),
                self.functions[i + 1](self.intervals[i + 1].dmin),
            ):
                return False
        return True

    def apply(self, x: float) -> float:
        """Apply function to single value.

        :param x:
        :raises ValueError: if `x` is not inside an interval
        :return:
        """
        for interval, f in zip(self.intervals, self.functions):
            if x in interval:
                return f(x)
        raise ValueError(
            f"cannot apply piecewise function to out-of-bound value: {x}"
        )

    def __call__(self, x: float) -> float:
        """Apply function to single value.

        :param x:
        :raises ValueError: if `x` is not inside an interval
        :return:
        """
        return self.apply(x)


class FuzzyNumber(PieceWiseFunction):
    """This class implements a trapezoidal fuzzy number.

    A fuzzy number is described by its 4 abscissa in increasing order.
    Its ordinates are fixed at ``[0, 1, 1, 0]``.

    Triangular fuzzy number can be represented by having two consecutive
    abscissa equals.

    :param abscissa: list of abscissa defining a trapezoidal fuzzy number
    :raises ValueError:
        * if abscissa has not exactly 4 values
        * if abscissa are not in increasing order
    """

    def __init__(
        self,
        abscissa: List[float],
    ):
        """Constructor method"""
        if len(abscissa) != 4:
            raise ValueError("FuzzyNumber must have 4 abscissa")
        self.abscissa = abscissa
        self.ordinates = [0, 1, 1, 0]
        segments = []
        for x1, x2, y1, y2 in zip(
            self.abscissa[:-1],
            self.abscissa[1:],
            self.ordinates[:-1],
            self.ordinates[1:],
        ):
            if x1 > x2:
                raise ValueError(
                    "FuzzyNumber abscissa must be in increasing order"
                )
            if x1 < x2:
                segments.append([[x1, y1], [x2, y2]])
        if len(segments) == 0:
            PieceWiseFunction.__init__(
                self,
                [Interval(self.abscissa[0], self.abscissa[0])],
                [lambda x: 1],
            )
        else:
            PieceWiseFunction.__init__(self, segments=segments)

    def __eq__(self, other) -> bool:
        """Test equality of objects.

        :param other:
        :return:
        """
        if type(other) != type(self):
            return False
        _fuzzy = cast(FuzzyNumber, other)
        return self.abscissa == _fuzzy.abscissa

    def apply(self, x: float) -> float:
        """Apply function to single value.

        :param x:
        :return:

        .. note:: returns ``0`` if value is not in the fuzzy set
        """
        for interval, f in zip(self.intervals, self.functions):
            if x in interval:
                return f(x)
        return 0

    @property
    def average(self) -> float:
        """Computes the average of all intervals boundaries.

        :return:
        """
        res = self.intervals[0].dmin
        for interval in self.intervals:
            res += interval.dmax
        return res / (len(self.functions) + 1)

    @property
    def centre_of_gravity(self) -> float:
        """Computes the centre of gravity of this fuzzy set (COG).

        :return: the x value of COG
        """
        if self.abscissa[0] == self.abscissa[3]:
            y = 0.5
        else:
            y = (1 / 6) * (
                (self.abscissa[2] - self.abscissa[1])
                / (self.abscissa[3] - self.abscissa[0])
                + 2
            )
        return (
            y * (self.abscissa[2] + self.abscissa[1])
            + (self.abscissa[3] + self.abscissa[0]) * (1 - y)
        ) / 2

    @property
    def centre_of_maximum(self) -> float:
        """Returns the centre of maximum of this fuzzy set (COM).

        :return:
        """
        return (self.abscissa[2] + self.abscissa[1]) / 2

    @property
    def area(self) -> float:
        """Returns the area under the fuzzy number curve.

        :return:
        """
        return (
            (self.abscissa[3] - self.abscissa[0])
            + (self.abscissa[2] - self.abscissa[1])
        ) / 2
