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

    def test_averages_player_count_per_server_per_rounded_minute(self):

        self._record_player_counts((
            (second('00:12'), 10, 1),
            (second('00:59'), 20, 1),
            (second('01:00'), 30, 1),
            (second('01:30'), 30, 1),
            (second('05:01'), 30, 1),
            (second('05:02'), 35, 1)
        ))

        expected = {
            second('00:00'): 10,
            second('01:00'): 25,
            second('02:00'): 30,
            second('05:00'): 32.5
        }

        actual_counts = self._extract_actual_counts_for('server01')

        self.assertEqual(expected, actual_counts)

    def test_sums_total_player_count_across_servers(self):

        self._record_player_counts((
            (second('00:12'), 10, 1),
            (second('00:59'), 10, 1),
            (second('01:00'), 20, 2),
            (second('01:40'), 10, 1),
            (second('01:50'), 20, 2),
            (second('02:00'), 30, 3)
        ))

        expected = {
            second('00:00'): 10,
            second('01:00'): 30,
            second('02:00'): 60
        }

        actual_sum = self._extract_actual_counts_for('total')

        self.assertEqual(expected, actual_sum)

    def test_reports_player_count_per_server(self):

        self._record_player_counts((
            (second('00:12'), 10, 1),
            (second('00:59'), 10, 1),
            (second('01:00'), 20, 2),
            (second('01:40'), 10, 1),
            (second('01:50'), 20, 2),
            (second('02:00'), 30, 3)
        ))

        expected_server_1 = {
            second('00:00'): 10,
            second('01:00'): 10,
            second('02:00'): 10
        }

        actual = self._extract_actual_counts_for('server01')

        self.assertEqual(expected_server_1, actual)

    def _record_player_counts(self, records):
        for record in records:
            self.sut.record_player_count(record[0], record[1], record[2])
        self.sut.write_all()

    def _extract_actual_counts_for(self, key):
        counts_for_key = {}
        for minute, counts in self.sut.total_player_counts().items():
            counts_for_key[minute] = counts[key]
        return counts_for_key

    def _record_character(self, character_id, sex,
                          birth=default_birth,
                          death=default_birth + timedelta(minutes=60),
                          mom_id=None):
        self.sut.record_birth(character_id, birth, mom_id, sex)
        self.sut.record_death(character_id, death)
