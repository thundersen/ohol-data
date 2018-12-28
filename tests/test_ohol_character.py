import unittest

from datetimerange import DateTimeRange

from logreader.ohol_character import FERTILE_END_EVE
from tests.character_factories import *
from tests.time_factories import minute


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

        self.assertSequenceEqual(range(14, 40+1), minutes)

    def test_fertile_minutes_are_round(self):
        sut = female(birth=minute('01:27'))

        result = sut.fertile_mom_minutes()

        seconds = list(set([m.second for m in result]))

        self.assertSequenceEqual([0], seconds)

    def test_died_as_kid_has_no_fertile_minutes(self):
        sut = female(death=default_birth + timedelta(minutes=13))

        self.assertListEqual(sut.fertile_mom_minutes(), [])

    def test_died_fertile_reduces_fertile_minutes(self):
        sut = female(death=default_birth + timedelta(minutes=20))

        minutes = [m.minute for m in sut.fertile_mom_minutes()]

        self.assertSequenceEqual(range(14, 20+1), minutes)

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

    def test_eve_fertility(self):
        sut = eve()

        self.assertEqual(
            DateTimeRange(sut.birth, sut.birth + FERTILE_END_EVE),
            sut.fertility_period())
