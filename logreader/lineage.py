from datetimerange import DateTimeRange


class Lineage:
    def __init__(self, eve):
        self.eve = eve

    def __str__(self):
        return '%s | %s' % (self.duration(), self.eve)

    def id(self):
        return self.eve.id

    def characters(self):
        return [self.eve] + self.eve.descendants()

    def duration(self):
        incomplete_characters = [c for c in self.characters() if not c.is_complete()]

        if len(incomplete_characters) > 0:
            print('ERROR: incomplete lineage %s (%s incomplete members; eve birth: %s)' % (self.id(), len(incomplete_characters), self.eve.birth))
            return None

        last_fertility_end = max(d.fertility_period().end_datetime for d in self.characters())

        return DateTimeRange(self.eve.birth, last_fertility_end)


