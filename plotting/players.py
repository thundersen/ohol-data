from datetime import date

from plotly import tools
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters

SERVERS = [1, 2, 3, 4, 5, 6, 7]

# START = date(2018, 4, 1)
START = date(2018, 10, 1)
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

    ratio_less = float(n_less_than_threshold / n_players)

    print(f'filtered out {n_less_than_threshold} of {n_players} ({100*ratio_less}%) '
          f'who played less then {threshold_hours} hours')

    return go.Histogram(y=at_least_threshold, nbinsy=15, showlegend=False)


def print_top_ten(players):
    top_ten = reversed(sorted(players, key=lambda p: p.total_playtime())[-10:])
    top_ten_table = [(to_hours_per_day(p.total_playtime()), p.favorite_eve_name()) for p in top_ten]
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


if __name__ == '__main__':
    history = read_characters(SERVERS, START, END)

    players = history.all_players()

    n_players = len(players)

    print(f'{n_players} players recognized')

    threshold_hours = .5

    playtime_trace = make_playtime_trace(players, threshold_hours)

    fig = tools.make_subplots(
        rows=2, cols=1,
        subplot_titles=[f'Avg. Hours per Day for Players with at Least {threshold_hours} Hours per Day',
                        'New Players'])

    fig['layout'].update(title=f'Players from {START} to {END} on Servers {", ".join([str(s) for s in SERVERS])}')

    first_birth_trace = go.Histogram(x=[p.first_birth() for p in players], showlegend=False)

    fig.append_trace(playtime_trace, 1, 1)
    fig.append_trace(first_birth_trace, 2, 1)

    py.plot(fig)
