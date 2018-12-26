import unittest
from datetime import timedelta

from datetimerange import DateTimeRange

from logreader.lineage import Lineage
from tests.character_factories import eve, female


class TestLineage(unittest.TestCase):
    def test_duration_at_least_eve_fertility(self):
        e = eve()
        sut = Lineage(e)

        self.assertEqual(e.fertility_period(), sut.duration())

    def test_duration_is_eve_birth_to_max_fertility_end_of_girls(self):
        e = eve()
        daughter = female(birth=e.birth + timedelta(minutes=5))
        e.add_kid(daughter)
        granddaughter = female(birth=daughter.birth + timedelta(minutes=20))
        daughter.add_kid(granddaughter)

        sut = Lineage(e)

        expected = DateTimeRange(e.birth, granddaughter.fertility_period().end_datetime)
        self.assertEqual(expected, sut.duration())

