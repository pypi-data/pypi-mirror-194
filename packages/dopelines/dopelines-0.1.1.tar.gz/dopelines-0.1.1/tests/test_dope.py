from unittest import TestCase
import numpy
from dope import normalize, distance_point_to_line, DoPeR

SHOW_PLOTS = False


class NormalizeTests(TestCase):
    def test_normalize(self):
        rng = numpy.random.default_rng()
        data = 10 * rng.standard_normal((10, 2)) + numpy.array([-100, 100])
        normalized = normalize(data)
        self.assertTrue(numpy.all(normalized.min(axis=0, initial=None) == 0))
        self.assertTrue(numpy.all(normalized.max(axis=0, initial=None) == 1))


class DistancePointToLineTests(TestCase):
    def test_distance_point_to_line(self):
        actual_distance = 2
        line_segment_length = 3
        line = numpy.array([[0, 0], [0, line_segment_length]])
        point = numpy.array([actual_distance, 0])
        cases = [point, numpy.vstack((point, point))]
        for case in cases:
            with self.subTest(case=case):
                distances = distance_point_to_line(point=case, line=line)
                self.assertTrue(numpy.all(distances == actual_distance))


class DoPeRTests(TestCase):
    def setUp(self) -> None:
        # dummy data
        x = range(8)
        y = [0, -1, 2, 0, 0, -1, 1, 0]
        self.data = list(zip(x, y))

    def test_max_length(self):
        """may be obvious, may be not"""
        dp = DoPeR(data=self.data)
        cases = [(0, 2), (1, 3), (2, 5), (3, 9), (4, 17)]
        for max_depth, expected_max_length in cases:
            dp.max_depth = max_depth
            self.assertEqual(expected_max_length, dp.max_length)

    def test_simplify_tolerance(self):
        dp = DoPeR(data=self.data)
        cases = [
            (0.0, 8),
            (0.1, 8),
            (0.2, 6),
            (0.3, 5),
            (0.4, 4),
            (0.5, 3),
            (0.6, 3),
            (0.7, 2),
            (1.0, 2),
        ]
        for tolerance, expected_length in cases:
            with self.subTest(msg=tolerance):
                simplified = dp.simplify(tolerance=tolerance)
                if SHOW_PLOTS:
                    dp.plot()
                self.assertEqual(expected_length, simplified.shape[0])

    def test_simplify_max_depth(self):
        dp = DoPeR(data=self.data)
        cases = [0, 1, 2, 3, 4]
        for max_depth in cases:
            with self.subTest(msg=max_depth):
                simplified = dp.simplify(max_depth=max_depth)
                if SHOW_PLOTS:
                    dp.plot(normalized=False)
                self.assertLessEqual(simplified.shape[0], dp.max_length)
