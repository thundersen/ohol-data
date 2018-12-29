import unittest
from datetime import date

from download_lifelogs import build_names


class TestDownloadLifelogs(unittest.TestCase):

    def test_filenames_are_correct(self):
        result = build_names([1, 2], date(2018, 12, 9), date(2018, 12, 10))

        expected = [
            'lifeLog_server1.onehouronelife.com/2018_12December_09_Sunday.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_09_Sunday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_09_Sunday.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_09_Sunday_names.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_10_Monday.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_10_Monday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_10_Monday.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_10_Monday_names.txt'
        ]
        self.maxDiff = None
        self.assertSequenceEqual(expected, result)
