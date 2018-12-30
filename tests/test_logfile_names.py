import unittest
from datetime import date

from download_lifelogs import build_names


class TestDownloadLifelogs(unittest.TestCase):

    def test_filenames_are_correct(self):
        result = build_names([1, 2], date(2018, 9, 30), date(2018, 10, 1))

        expected = [
            'lifeLog_server1.onehouronelife.com/2018_09September_30_Sunday.txt',
            'lifeLog_server1.onehouronelife.com/2018_09September_30_Sunday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_09September_30_Sunday.txt',
            'lifeLog_server2.onehouronelife.com/2018_09September_30_Sunday_names.txt',
            'lifeLog_server1.onehouronelife.com/2018_10October_01_Monday.txt',
            'lifeLog_server1.onehouronelife.com/2018_10October_01_Monday_names.txt',
            'lifeLog_server2.onehouronelife.com/2018_10October_01_Monday.txt',
            'lifeLog_server2.onehouronelife.com/2018_10October_01_Monday_names.txt'
        ]
        self.maxDiff = None
        self.assertSequenceEqual(expected, result)
