import datetime
import collections

from logreader.character import UNKNOWN_NAME


def _strip_number_from_name(raw_name):
    split = raw_name.split()
    return " ".join(split[:2]) if len(split) > 2 else raw_name


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.characters = []

    def __str__(self):
        return f'{self.player_id} {len(self.characters)} lives'

    def add_character(self, character):
        self.characters.append(character)

    def total_playtime(self):
        durations = [c.death - c.birth for c in self.characters if c.birth is not None and c.death is not None]
        return sum(durations, datetime.timedelta())

    def first_birth(self):
        return min([c.birth for c in self.characters])

    def last_death(self):
        return max([c.death for c in self.characters])

    def favorite_eve_name(self, top=1):
        eve_names = [_strip_number_from_name(c.name) for c in self.characters
                     if c.is_eve and c.name is not UNKNOWN_NAME]

        if len(eve_names) == 0:
            return UNKNOWN_NAME

        counts = collections.Counter(eve_names).most_common(top)
        return ', '.join([name for name, count in counts])

    def days_played(self):
        return set([c.birth.date() for c in self.characters])


