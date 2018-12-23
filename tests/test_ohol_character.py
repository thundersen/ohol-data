import unittest
from datetime import datetime, timedelta

from logreader.ohol_character import OholCharacter

default_birth = datetime(2019, 1, 1)


# noinspection PyTypeChecker
def surviving_mom_with_daughter():
    sut = female()
    sut.kids.append('ABC')
    sut.read_kids({
        'ABC': female(id='ABC')
    })
    return sut


def surviving_mom_with_only_boys():
    sut = female()
    sut.kids = ['DEF']
    sut.read_kids({
        'DEF': male(id='DEF')
    })
    return sut


def surviving_mom_with_no_kids():
    sut = female()
    sut.read_kids({
        'DEF': male(id='DEF')
    })
    return sut


class TestOholCharacter(unittest.TestCase):
    def test_is_complete_when_birth_and_death_present(self):
        sut = female()

        self.assertTrue(sut.is_complete())

    def test_is_not_complete_when_birth_missing(self):
        sut = female()
        sut.birth = None

        self.assertFalse(sut.is_complete())

    def test_is_not_complete_when_death_missing(self):
        sut = female()
        sut.death = None

        self.assertFalse(sut.is_complete())

    def test_fertile_minutes_is_empty_for_male(self):
        sut = male()

        self.assertListEqual(sut.fertile_mom_minutes(), [])

    def test_fertile_minutes_are_age_14_through_40(self):
        sut = female()

        minutes = [m.minute for m in sut.fertile_mom_minutes()]

        self.assertSequenceEqual(range(14, 40), minutes)

    def test_fertile_minutes_are_round(self):
        sut = female(birth=minute('01:27'))

        result = sut.fertile_mom_minutes()

        seconds = [m.second for m in result]

        self.assertListEqual(26 * [0], seconds)

    def test_died_as_kid_has_no_fertile_minutes(self):
        sut = female(death=default_birth + timedelta(minutes=13))

        self.assertListEqual(sut.fertile_mom_minutes(), [])

    def test_died_fertile_reduces_fertile_minutes(self):
        sut = female(death=default_birth + timedelta(minutes=20))

        minutes = [m.minute for m in sut.fertile_mom_minutes()]

        self.assertSequenceEqual(range(14, 20), minutes)

    def test_mom_survived_fertility_with_no_kids_is_0girls(self):
        self.assertTrue(surviving_mom_with_no_kids().is_zero_girl_mom())

    def test_mom_survived_fertility_with_no_kids_is_not_mom_with_girls(self):
        self.assertFalse(surviving_mom_with_no_kids().is_mom_with_girls())

    def test_mom_survived_fertility_with_only_boys_is_0girls(self):
        self.assertTrue(surviving_mom_with_only_boys().is_zero_girl_mom())

    def test_mom_survived_fertility_with_only_boys_is_not_mom_with_girls(self):
        self.assertFalse(surviving_mom_with_only_boys().is_mom_with_girls())

    def test_mom_survived_fertility_with_a_daughter_is_not_0girls(self):
        self.assertFalse(surviving_mom_with_daughter().is_zero_girl_mom())

    def test_mom_survived_fertility_with_a_daughter_is_mom_with_girls(self):
        self.assertTrue(surviving_mom_with_daughter().is_mom_with_girls())

    def test_mom_died_before_40_without_daughters_is_not_0girls(self):
        self.assertFalse(female(death=default_birth + timedelta(minutes=30)).is_zero_girl_mom())

    def test_mom_died_before_40_without_daughters_is_not_mom_with_girls(self):
        self.assertFalse(female(death=default_birth + timedelta(minutes=30)).is_mom_with_girls())

    def test_male_is_not_considered_0girls(self):
        self.assertFalse(male().is_zero_girl_mom())

    def test_male_is_not_considered_mom_with_girls(self):
        self.assertFalse(male().is_mom_with_girls())


def female(id='123', birth=default_birth, death=None):
    sut = OholCharacter(id)
    sut.birth = birth
    sut.death = (birth + timedelta(minutes=60)) if death is None and birth is not None else death
    sut.sex = 'F'
    return sut


def male(id='123', birth=default_birth, death=None):
    sut = female(id, birth, death)
    sut.sex = 'M'
    return sut


def make_character(param):
    split = param.split()
    character = OholCharacter(split[0])
    character.sex = split[1]
    character.birth = hour(split[2])
    character.death = hour(split[3])
    return character


def minute(minute_string):
    return hour('00:' + minute_string)


def hour(hour_string):
    return datetime.strptime('2019-01-01 %s' % hour_string, '%Y-%m-%d %H:%M:%S')
