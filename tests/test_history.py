import unittest
from datetime import datetime

from logreader.history import History

default_birth = datetime(2019, 1, 1)


class TestHistory(unittest.TestCase):

    def test_tracks_lineages(self):
        sut = History()
        sut.record_birth('1', default_birth, None, 'F')
        sut.record_birth('2', default_birth, None, 'F')

        self.assertEqual(len(sut.all_lineages()), 2)

    def test_assigns_eve_kids_to_lineage(self):
        sut = History()
        sut.record_birth('1', default_birth, None, 'F')
        sut.record_birth('2', default_birth, '1', 'F')

        self.assertEqual(len(sut.all_lineages()), 1)
        self.assertEqual(len(sut.lineage('1').characters()), 2)

    def test_assigns_all_eve_descendants_to_lineage(self):
        sut = History()
        sut.record_birth('1', default_birth, None, 'F')
        sut.record_birth('2', default_birth, '1', 'F')
        sut.record_birth('3', default_birth, '2', 'M')
        sut.record_birth('4', default_birth, '2', 'F')
        sut.record_birth('5', default_birth, '4', 'M')

        self.assertEqual(len(sut.all_lineages()), 1)
        self.assertEqual(len(sut.lineage('1').characters()), 5)
