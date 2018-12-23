from datetime import timedelta

from timeutils.timeutils import round_minute_range


FERTILE_START = timedelta(minutes=14)
FERTILE_END = timedelta(minutes=40)


class OholCharacter:
    def __init__(self, id, name='[UNKNOWN]'):
        self.sex = None
        self.death = None
        self.birth = None
        self.id = id
        self.name = name
        self.kids = []
        self.is_eve = False
        self.daughters = []
        self.sons = []

    def __str__(self):
        return self.id + " | " + self.name + " | " + str(self.birth) + " - " + str(self.death) \
            + " | kids: " + ",".join(self.kids)

    def is_complete(self):
        return self.birth is not None and self.death is not None

    def fertile_mom_minutes(self):
        if self.sex is not 'F' or not self.is_complete():
            return []

        return round_minute_range(self.fertility_start(), self.fertility_end())

    def fertility_end(self):
        return min(self.death, self.birth + FERTILE_END)

    def fertility_start(self):
        return self.birth + FERTILE_START

    def add_kid(self, kid_id):
        self.kids.append(kid_id)

    def mark_as_eve(self):
        self.is_eve = True

    def is_zero_girl_mom(self):
        return self.is_surviving_mom() and not self.has_daughters()

    def has_outlived_fertility(self):
        return self.is_complete() and (self.death - self.birth) > FERTILE_END

    def read_kids(self, characters):
        for kid_id in self.kids:
            if characters[kid_id].sex == 'F':
                self.daughters.append(kid_id)
            elif characters[kid_id].sex == 'M':
                self.sons.append(kid_id)
            else:
                print('ERROR: kid with unknown sex ' + characters[kid_id])

    def is_mom_with_girls(self):
        return self.is_surviving_mom() and self.has_daughters()

    def has_daughters(self):
        return len(self.daughters) > 0

    def is_surviving_mom(self):
        return self.sex == 'F' and self.has_outlived_fertility()


