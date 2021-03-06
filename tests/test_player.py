import unittest
from datetime import datetime, timedelta, date

from logreader.player import Player
from tests.character_factories import female, eve


class TestPlayer(unittest.TestCase):
    def test_sums_up_playtime(self):
        sut = Player('Someone')
        sut.add_character(female(birth=datetime(2019, 1, 1, 0, 0, 0), death=datetime(2019, 1, 1, 1, 0, 0)))
        sut.add_character(female(birth=datetime(2019, 1, 1, 2, 0, 0), death=datetime(2019, 1, 1, 3, 0, 0)))

        self.assertEqual(timedelta(hours=2), sut.total_playtime())

    def test_reports_first_birth(self):
        sut = Player('Someone')
        first_birth = datetime(2019, 1, 1, 0, 0, 0)
        sut.add_character(female(birth=datetime(2019, 1, 1, 2, 0, 0)))
        sut.add_character(female(birth=first_birth))
        sut.add_character(female(birth=datetime(2019, 1, 1, 3, 0, 0)))
        sut.add_character(female(birth=datetime(2019, 1, 1, 4, 0, 0)))

        self.assertEqual(first_birth, sut.first_birth())

    def test_reports_last_death(self):
        sut = Player('Someone')
        last_death = datetime(2019, 1, 1, 4, 0, 0)
        sut.add_character(female(death=datetime(2019, 1, 1, 2, 0, 0)))
        sut.add_character(female(death=last_death))
        sut.add_character(female(death=datetime(2019, 1, 1, 3, 0, 0)))
        sut.add_character(female(death=datetime(2019, 1, 1, 1, 0, 0)))

        self.assertEqual(last_death, sut.last_death())

    def test_reports_favorite_eve_name(self):
        sut = Player('Someone')
        sut.add_character(eve(name='EVE ILL'))
        sut.add_character(eve(name='EVE ILL II'))
        sut.add_character(eve(name='EVE EIGENRAUCH'))
        sut.add_character(female(name='HOPE'))
        sut.add_character(female(name='HOPE'))
        sut.add_character(female(name='HOPE'))

        self.assertEqual('EVE ILL', sut.favorite_eve_name())

    def test_reports_top_favorite_eve_names(self):
        sut = Player('Someone')
        sut.add_character(eve(name='EVE ILL'))
        sut.add_character(eve(name='EVE ILL II'))
        sut.add_character(eve(name='EVE EIGENRAUCH'))
        sut.add_character(eve(name='EVE GRIEF'))
        sut.add_character(eve(name='EVE GRIEF'))
        sut.add_character(eve(name='EVE GRIEF'))

        self.assertEqual('EVE GRIEF, EVE ILL', sut.favorite_eve_name(top=2))

    def test_reports_days_played(self):
        sut = Player('Someone')
        sut.add_character(female(birth=datetime(2019, 1, 1, 1, 0, 0)))
        sut.add_character(female(birth=datetime(2019, 1, 1, 2, 0, 0)))
        sut.add_character(female(birth=datetime(2019, 1, 2)))
        sut.add_character(female(birth=datetime(2018, 12, 31)))

        expected = {date(2018, 12, 31), date(2019, 1, 1), date(2019, 1, 2)}
        self.assertSequenceEqual(expected, sut.days_played())
