import unittest
from datetime import datetime, timedelta

from logreader.history import History
from tests.test_timeutils import second

default_birth = datetime(2019, 1, 1)


class TestHistory(unittest.TestCase):

    def setUp(self):
        self.sut = History()

    def test_tracks_lineages(self):
        self._record_character('1', 'F')
        self._record_character('2', 'F')

        self.sut.write_all()

        self.assertEqual(len(self.sut.all_lineages()), 2)

    def test_assigns_eve_kids_to_lineage(self):
        self._record_character('1', 'F')
        self._record_character('2', 'F', mom_id='1')

        self.sut.write_all()

        self.assertEqual(len(self.sut.all_lineages()), 1)
        self.assertEqual(len(self.sut.lineage('1').characters()), 2)

    def test_assigns_all_eve_descendants_to_lineage(self):
        self._record_character('1', 'F')
        self._record_character('2', 'F', mom_id='1')
        self._record_character('3', 'F', mom_id='2')
        self._record_character('4', 'F', mom_id='2')
        self._record_character('5', 'F', mom_id='4')

        self.sut.write_all()

        self.assertEqual(len(self.sut.all_lineages()), 1)
        self.assertEqual(len(self.sut.lineage('1').characters()), 5)

    def test_records_player_count_per_rounded_minute(self):
        self.sut.record_player_count(second('00:12'), 10)
        self.sut.record_player_count(second('00:59'), 20)
        self.sut.record_player_count(second('01:00'), 30)
        self.sut.record_player_count(second('01:30'), 30)
        self.sut.record_player_count(second('05:01'), 30)
        self.sut.record_player_count(second('05:02'), 35)
        self.sut.write_all()

        expected = {
            second('00:00'): 10,
            second('01:00'): 25,
            second('02:00'): 30,
            second('05:00'): 32.5
        }

        self.assertEqual(expected, self.sut.player_counts())

    def _record_character(self, character_id, sex,
                          birth=default_birth,
                          death=default_birth + timedelta(minutes=60),
                          mom_id=None):
        self.sut.record_birth(character_id, birth, mom_id, sex)
        self.sut.record_death(character_id, death)
