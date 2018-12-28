from timeutils.timeutils import round_minute


def _current_average(count, avg_count_per_minute_so_far, n_counts_per_minute_so_far):
    sum_of_counts = float((avg_count_per_minute_so_far * n_counts_per_minute_so_far + count))
    return sum_of_counts / (n_counts_per_minute_so_far + 1)


class PlayerCountTracker:

    def __init__(self):
        self._raw_player_counts = {}
        self._player_counts = {}

    def record_player_count(self, timestamp, count):
        self._raw_player_counts[timestamp] = count

    def player_counts(self):
        return self._player_counts

    def write_player_counts(self):
        n_counts_per_minute = {}

        for time, count in self._raw_player_counts.items():
            minute = round_minute(time)

            if minute not in n_counts_per_minute:
                n_counts_per_minute[minute] = 0

            if minute not in self._player_counts:
                self._player_counts[minute] = count
            else:
                self._player_counts[minute] = \
                    _current_average(count, self._player_counts[minute], n_counts_per_minute[minute])

            n_counts_per_minute[minute] += 1
