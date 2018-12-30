from datetime import timedelta

from datetimerange import DateTimeRange


class Lineage:

    max_descendants = 0
    max_duration = timedelta(seconds=0)

    def __init__(self, eve):
        self.eve = eve

        eve_descendants = self.eve.descendants()

        self._characters = [self.eve] + eve_descendants

        self._log_max_eve_descendants(eve_descendants)

        self._duration = self._calculate_duration()

        self._log_max_duration()

    def _log_max_eve_descendants(self, eve_descendants):
        if len(eve_descendants) > Lineage.max_descendants:
            Lineage.max_descendants = len(eve_descendants)
            print(
                f'max descendants so far: {Lineage.max_descendants} '
                f'for {self.eve.name} ({self.id()}) born at {self.eve.birth}')

    def _log_max_duration(self):
        if self._duration.timedelta > Lineage.max_duration:
            Lineage.max_duration = self._duration.timedelta
            print(
                f'max duration so far: {Lineage.max_duration} '
                f'for {self.eve.name} ({self.id()}) born at {self.eve.birth}')

    def __str__(self):
        return '%s | %s' % (self.duration(), self.eve)

    def id(self):
        return self.eve.id

    def characters(self):
        return self._characters

    def duration(self):
        return self._duration

    def _calculate_duration(self):
        last_fertility_end = max(d.fertility_period().end_datetime for d in self.characters())
        return DateTimeRange(self.eve.birth, last_fertility_end)




