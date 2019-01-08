from datetime import date

import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters

SERVERS = [1, 2, 3, 4, 5, 6, 7]

START = date(2018, 12, 28)
END = date(2018, 12, 31)

N_DAYS = (END - START).days + 1


def to_hours_per_day(td):
    return (td.days * 24 + float(td.seconds) / 3600) / N_DAYS


def make_playtime_trace(players, threshold_hours):
    time_played = [to_hours_per_day(p.total_playtime()) for p in players]

    print_top_ten(players)

    at_least_threshold = [t for t in time_played if t >= threshold_hours]

    less_than_threshold = [t for t in time_played if t < threshold_hours]

    n_less_than_threshold = len(less_than_threshold)

    ratio_less = float(n_less_than_threshold / len(players))

    print(f'filtered out {n_less_than_threshold} of {len(players)} ({100*ratio_less}%) '
          f'who played less then {threshold_hours} hours')

    return go.Histogram(y=at_least_threshold, nbinsy=15, showlegend=False)


def print_top_ten(players):
    n_eve_names = 3
    top_ten = list(reversed(sorted(players, key=lambda p: p.total_playtime())[-10:]))
    top_ten_table = [(to_hours_per_day(p.total_playtime()), p.favorite_eve_name(top=n_eve_names)) for p in top_ten]
    print('TOP TEN')
    print('=======')
    spot = 1
    for p in top_ten_table:
        spot_string = str(spot) + '.'
        if spot < 10:
            spot_string = ' ' + spot_string

        hours_string = str(round(p[0], 2))
        if p[0] < 10:
            hours_string = ' ' + hours_string

        print(f'{spot_string} {hours_string} {p[1]}')
        spot += 1


def read_players():
    history = read_characters(SERVERS, START, END)
    history.print_completeness_report()
    players = history.all_players()
    n_players = len(players)
    print(f'{n_players} players recognized')
    return players


if __name__ == '__main__':
    players = read_players()

    threshold_hours = .5

    playtime_trace = make_playtime_trace(players, threshold_hours)

    title = f'Avg. Hours per Day for Players with at Least {threshold_hours} Hours per Day' \
            f'from {START} to {END} on Servers {", ".join([str(s) for s in SERVERS])}'

    py.plot({'data': [playtime_trace], 'layout': {'title': title, 'title2': 'bla'}})
