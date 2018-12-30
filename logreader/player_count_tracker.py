from timeutils.timeutils import round_minute


def _current_average(count, avg_count_per_minute_so_far, n_counts_per_minute_so_far):
    sum_of_counts = float((avg_count_per_minute_so_far * n_counts_per_minute_so_far + count))
    return sum_of_counts / (n_counts_per_minute_so_far + 1)


class PlayerCountTracker:

    def __init__(self):
        self._raw_player_counts = {}
        self._player_counts = {}

    def record_player_count(self, timestamp, count, server_no):
        if server_no not in self._raw_player_counts:
            self._raw_player_counts[server_no] = {}

        self._raw_player_counts[server_no][timestamp] = count

    def player_counts(self):
        return self._player_counts

    def write_player_counts(self):

        counts_per_minute_per_server = self._calculate_counts_per_minute_per_server()

        for minute, server_counts in counts_per_minute_per_server.items():
            self._player_counts[minute] = {'total': sum(server_counts.values())}

            for server in server_counts:
                self._player_counts[minute][f'server{server:02d}'] = server_counts[server]

    def _calculate_counts_per_minute_per_server(self):
        counts_per_minute_per_server = {}
        for server, counts in self._raw_player_counts.items():

            n_counts_per_minute = {}

            for time, count in counts.items():

                minute = round_minute(time)

                if minute not in n_counts_per_minute:
                    n_counts_per_minute[minute] = 0

                if minute not in counts_per_minute_per_server:
                    counts_per_minute_per_server[minute] = {}

                if server not in counts_per_minute_per_server[minute]:
                    counts_per_minute_per_server[minute][server] = count
                else:
                    avg_before = counts_per_minute_per_server[minute][server]
                    counts_per_minute_per_server[minute][server] = \
                        _current_average(count, avg_before, n_counts_per_minute[minute])

                n_counts_per_minute[minute] += 1
        return counts_per_minute_per_server
