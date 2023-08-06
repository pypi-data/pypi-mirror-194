import sys
from typing import List, Optional

try:
    from matplotlib import pyplot as plt
except ImportError:
    plt = None
import numpy
import numpy.typing

# single source of truth for package version
# https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
# https://semver.org/
__version__ = '0.1.1'

RECURSION_LIMIT = sys.getrecursionlimit()


def normalize(data: numpy.ndarray) -> numpy.ndarray:
    """Transform data columns so their values are between zero and one."""
    return (data - data.min(axis=0, initial=None)) / data.ptp(axis=0)


def distance_point_to_line(point, line):
    """
    Distance from one (or more) point(s) to a line defined by two nodes.

    point = [x0, y0]  (can also be an m x 2 array of points)
    line = [[x1, y1], [x2, y2]]

    distance = abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1)) / sqrt((x2-x1)^2+(y2-y1)^2)

    reference:

    https://mathworld.wolfram.com/Point-LineDistance2-Dimensional.html
    """
    if point.ndim == 1:
        point.resize((1, 2))
    s = numpy.diff(line, n=1, axis=0)
    numerator = numpy.abs(
        s[0, 0] * (line[0, 1] - point[:, 1])
        - (line[0, 0] - point[:, 0]) * s[0, 1]
    )
    denominator = numpy.sqrt(numpy.dot(s[0], s[0]))
    return numerator / denominator


class _DoPe(object):
    """
    Base class for Douglas-Peucker line simplification.

    (Not using abc?)
    """

    def __init__(self, data: numpy.typing.ArrayLike):
        self.data = numpy.array(data)
        self.data_normalized = normalize(self.data)
        self.tolerance = None
        self.max_depth = RECURSION_LIMIT
        self.indices = None

    @property
    def max_length(self):
        raise NotImplemented('must be implemented by child class')

    def plot(self, normalized=True):
        """Plot data and simplified line, for verification."""
        data = self.data_normalized
        if not normalized:
            data = self.data
        if plt:
            plt.plot(
                data[:, 0],
                data[:, 1],
                color='0.7',
            )
            plt.plot(
                data[self.indices, 0],
                data[self.indices, 1],
                color='r',
                linestyle=':',
                marker='o',
            )
            if normalized and self.tolerance:
                # plot reference line for tolerance
                plt.plot(
                    [1 - self.tolerance, 1 - self.tolerance, 1, 1],
                    [0.01, 0, 0, 0.01],
                    color='k',
                    linestyle='-',
                    linewidth=2,
                )
                plt.text(0.9, 0.02, 'tolerance', horizontalalignment='center')
            plt.title(
                f'{"normalized" if normalized else "original"} units, '
                f'tolerance={self.tolerance}, '
                f'max_depth={self.max_depth}, '
                f'reduction: {data.shape[0]} to {self.indices.size}'
            )
            plt.grid()
            plt.axis('equal')
            plt.show()
        else:
            Warning('matplotlib not found, try installing extras: dope[plot]')


class DoPeR(_DoPe):
    """Recursive implementation of Douglas-Peucker line simplification."""

    @property
    def max_length(self) -> int:
        """
        Max. number of nodes in the simplified result (occurs if every
        recursion results in a split).
        """
        return 2**self.max_depth + 1

    def simplify(
        self,
        tolerance: Optional[float] = None,
        max_depth: Optional[int] = None,
        interval: Optional[List[int]] = None,
        _depth: int = 0,
    ) -> numpy.ndarray:
        """Recursive (depth-first) Douglas-Peucker line simplification."""
        # handle input arguments
        if tolerance is None:
            tolerance = 0
        self.tolerance = tolerance
        if max_depth is None or max_depth >= RECURSION_LIMIT:
            max_depth = RECURSION_LIMIT
        self.max_depth = max_depth
        if interval is None:
            interval = [0, self.data_normalized.shape[0] - 1]
            self.indices = numpy.array(interval)
        # calculate point-line distances
        distances = distance_point_to_line(
            point=self.data_normalized[interval[0] + 1 : interval[1], :],
            line=self.data_normalized[interval][:],
        )
        # evaluate conditions
        bottom_reached = not distances.size
        max_depth_reached = _depth == self.max_depth
        local_max_index = numpy.argmax(distances) if distances.size else None
        tolerance_reached = distances[local_max_index] < self.tolerance
        # return or split
        if bottom_reached or max_depth_reached or tolerance_reached:
            # base case
            pass
        else:
            # recursion case
            global_max_index = local_max_index + interval[0] + 1
            insert_index = numpy.nonzero(self.indices == interval[1])[0]
            # store the split node
            self.indices = numpy.insert(
                self.indices, insert_index, global_max_index
            )
            # split and evaluate both sides recursively
            _depth += 1
            self.simplify(
                tolerance=self.tolerance,
                max_depth=self.max_depth,
                interval=[interval[0], global_max_index],
                _depth=_depth,
            )
            self.simplify(
                tolerance=self.tolerance,
                max_depth=self.max_depth,
                interval=[global_max_index, interval[1]],
                _depth=_depth,
            )
        # return simplified array, for convenience
        return self.data[self.indices, :]


class DoPeI(_DoPe):
    """Iterative implementation of Douglas-Peucker line simplification."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplemented(
            'Iterative line simplification has not been implemented yet.'
        )
