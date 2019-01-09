from datetime import timedelta

from datetimerange import DateTimeRange

from timeutils.timeutils import round_minute_range

FERTILE_START = timedelta(minutes=14)
FERTILE_END = timedelta(minutes=40)
FERTILE_END_EVE = timedelta(minutes=26)
UNKNOWN_NAME = '[UNKNOWN]'


class Character:
    def __init__(self, kids, name=UNKNOWN_NAME, is_eve=False, **kwargs):
        self.kids = kids
        self.name = name
        self.id = kwargs['id']
        self.sex = kwargs['sex']
        self.birth = kwargs['birth']
        self.birth_coordinates = kwargs['birth_coordinates']
        self.death = kwargs['death']
        self.death_coordinates = kwargs['death_coordinates']
        self.is_eve = is_eve
        self.mom_id = kwargs['mom_id']
        self.player = kwargs['player']
        self.murderer = kwargs['murderer_id']
        self.murder_victims = kwargs['murder_victims']

    def __str__(self):
        return self.id + " | " + self.name + " | " + str(self.birth) + " - " + str(self.death)

    def is_complete(self):
        return self.birth is not None and self.death is not None

    def fertile_mom_minutes(self):
        if self.sex is not 'F' or not self.is_complete():
            return []

        return round_minute_range(self.fertility_start(), self.fertility_end())

    def fertility_end(self):
        actual_end = FERTILE_END if not self.is_eve else FERTILE_END_EVE
        return min(self.death, self.birth + actual_end)

    def fertility_start(self):
        return self.birth + FERTILE_START if not self.is_eve else self.birth

    def fertility_period(self):
        return DateTimeRange(self.fertility_start(), self.fertility_end())

    def daughters(self):
        return [k for k in self.kids if k.sex == 'F']

    def sons(self):
        return [k for k in self.kids if k.sex == 'M']

    def descendants(self):
        daughters_descendants = [descendant for daughter in self.daughters() for descendant in daughter.descendants()]

        return self.kids + daughters_descendants

    def is_zero_girl_mom(self):
        return self.is_surviving_mom() and not self.has_daughters()

    def has_outlived_fertility(self):
        return self.is_complete() and (self.death - self.birth) > FERTILE_END

    def is_mom_with_girls(self):
        return self.is_surviving_mom() and self.has_daughters()

    def has_daughters(self):
        return len(self.daughters()) > 0

    def is_surviving_mom(self):
        return self.sex == 'F' and self.has_outlived_fertility()

    def is_murderer(self):
        return len(self.murder_victims) > 0
