from datetime import date

import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_history
from timeutils.timeutils import date_range

SERVERS = [1, 2, 3, 4, 5, 6, 7]

START = date(2018, 10, 1)
END = date(2019, 1, 7)


def read_players():
    history = read_history(SERVERS, START, END)
    history.print_completeness_report()
    players = history.all_players()
    n_players = len(players)
    print(f'{n_players} players recognized')
    return players


def create_counts_per_day(players):
    result = {}

    for day in date_range(START, END):
        result[day] = 0

    for p in players:
        for day_played in p.days_played():
                result[day_played] = result[day_played] + 1

    return result


if __name__ == '__main__':
    players = read_players()

    first_birth_trace = go.Histogram(x=[p.first_birth() for p in players], name='First Seen')
    last_death_trace = go.Histogram(x=[p.last_death() for p in players], name='Last Seen')

    counts_per_day = create_counts_per_day(players)

    unique_players_trace = go.Scatter(x=list(counts_per_day.keys()), y=list(counts_per_day.values()), name='Total')

    title = f'OHOL Players from {START} to {END} on Servers {", ".join([str(s) for s in SERVERS])}'

    py.plot({'data': [first_birth_trace, last_death_trace, unique_players_trace], 'layout': {'title': title}})

    # first_vs_last_trace = go.Scatter(x=[p.last_death() for p in players], y=[p.first_birth() for p in players], name='First vs. Last Seen', mode='markers', opacity=.7)

    # py.plot([first_vs_last_trace])
