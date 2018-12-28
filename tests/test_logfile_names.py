import unittest
from datetime import date

from download_lifelogs import build_names


class TestDownloadLifelogs(unittest.TestCase):

    def test_filenames_are_correct(self):
        result = build_names([1, 2], date(2018, 12, 18), date(2018, 12, 19))

        expected = [
            'lifeLog_server1.onehouronelife.com/2018_12December_18_Tuesday.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_18_Tuesday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_18_Tuesday.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_18_Tuesday_names.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_19_Wednesday.txt',
            'lifeLog_server1.onehouronelife.com/2018_12December_19_Wednesday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_19_Wednesday.txt',
            'lifeLog_server2.onehouronelife.com/2018_12December_19_Wednesday_names.txt'
        ]
        self.maxDiff = None
        self.assertSequenceEqual(expected, result)
