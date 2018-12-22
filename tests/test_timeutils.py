import unittest
from datetime import datetime

from timeutils.timeutils import round_minute


class TestRoundMinute(unittest.TestCase):

    def test_already_round_minute_stays_same(self):
        self.assertEqual(second('01:00'), round_minute(second('01:00')))

    def test_lower_than_30_becomes_floor(self):
        self.assertEqual(second('01:00'), round_minute(second('01:29')))

    def test_30_becomes_ceiling(self):
        self.assertEqual(second('02:00'), round_minute(second('01:30')))


def second(minute_string):
    return datetime.strptime('2019-01-01 00:%s' % minute_string, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    unittest.main()
