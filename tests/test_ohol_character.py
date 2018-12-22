import unittest
from datetime import datetime, timedelta

from logreader.ohol_character import OholCharacter

default_birth = datetime(2019, 1, 1)


def make_female(birth=default_birth, death=default_birth + timedelta(minutes=60)):
    sut = OholCharacter('123')
    sut.birth = birth
    sut.death = death
    sut.sex = 'F'
    return sut


def make_male():
    sut = make_female()
    sut.sex = 'M'
    return sut


# noinspection PyTypeChecker
class TestOholCharacter(unittest.TestCase):
    def test_is_complete_when_birth_and_death_present(self):
        sut = make_female()

        self.assertTrue(sut.is_complete())

    def test_is_not_complete_when_birth_missing(self):
        sut = make_female(birth=None)

        self.assertFalse(sut.is_complete())

    def test_is_not_complete_when_death_missing(self):
        sut = make_female(death=None)

        self.assertFalse(sut.is_complete())

    def test_fertile_minutes_is_empty_for_male(self):
        sut = make_male()

        self.assertListEqual(sut.get_fertile_mom_minutes(), [])

    def test_fertile_minutes_are_age_14_through_40(self):
        sut = make_female()

        minutes = [m.minute for m in sut.get_fertile_mom_minutes()]

        self.assertSequenceEqual(range(14, 40), minutes)

    def test_fertile_minutes_are_round(self):
        sut = make_female(birth=second('01:27'))

        result = sut.get_fertile_mom_minutes()

        seconds = [m.second for m in result]

        self.assertListEqual(26 * [0], seconds)

    def test_died_as_kid_has_no_fertile_minutes(self):
        sut = make_female(death=default_birth + timedelta(minutes=13))

        self.assertListEqual(sut.get_fertile_mom_minutes(), [])

    def test_died_fertile_reduces_fertile_minutes(self):
        sut = make_female(death=default_birth + timedelta(minutes=20))

        minutes = [m.minute for m in sut.get_fertile_mom_minutes()]

        self.assertSequenceEqual(range(14, 20), minutes)


def second(minute_string):
    return datetime.strptime('2019-01-01 00:%s' % minute_string, '%Y-%m-%d %H:%M:%S')
