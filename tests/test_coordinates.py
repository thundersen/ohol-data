import unittest


from logreader.coordinates import Coordinates


class TestCoordinates(unittest.TestCase):

    def test_distance_for_identical_is_zero(self):
        a = Coordinates(10, 10)
        b = Coordinates(10, 10)

        self.assertEqual(0, a.distance_from(b))

    def test_distance(self):

        same_x = [
            ((0, 0), (0, 10), 10),
            ((10, 0), (0, 0), 10),
            ((-1, -1), (1, 1), 2.83)
        ]

        for p1, p2, expected_distance in same_x:
            a = Coordinates(p1[0], p1[1])
            b = Coordinates(p2[0], p2[1])
            with self.subTest(f'{a}, {b}'):
                self.assertEqual(expected_distance, round(a.distance_from(b), 2))

    def test_distance_from_zero(self):
        self.assertEqual(10, Coordinates(0, 10).distance_from_zero())
