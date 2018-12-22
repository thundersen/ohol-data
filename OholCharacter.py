from datetime import timedelta

from timeutils.timeutils import round_minute_range

AGE_FERTILE_START = 14
AGE_FERTILE_END = 40


class OholCharacter:
    def __init__(self, id, name='[UNKNOWN]'):
        self.sex = None
        self.death = None
        self.birth = None
        self.id = id
        self.name = name

    def __str__(self):
        return self.id + " | " + self.name + " | " + str(self.birth) + " - " + str(self.death)

    def is_complete(self):
        return self.birth is not None and self.death is not None

    def get_fertile_mom_minutes(self):
        if self.sex is not 'F' or not self.is_complete():
            return []

        return round_minute_range(self.fertility_start(), self.fertility_end())

    def fertility_end(self):
        return min(self.death, self.birth + timedelta(minutes=AGE_FERTILE_END))

    def fertility_start(self):
        return self.birth + timedelta(minutes=AGE_FERTILE_START)


