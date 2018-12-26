from datetimerange import DateTimeRange


class Lineage:
    def __init__(self, eve):
        self.eve = eve

    def __str__(self):
        return '%s | %s' % (self.duration(), self.eve)

    def characters(self):
        return [self.eve] + self.eve.descendants()

    def duration(self):
        last_fertility_end = max(d.fertility_period().end_datetime for d in self.characters())

        return DateTimeRange(self.eve.birth, last_fertility_end)


