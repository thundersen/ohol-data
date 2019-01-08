from datetime import date

import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters

SERVERS = [1, 2, 3, 4, 5, 6, 7]

START = date(2018, 10, 1)
END = date(2019, 1, 6)

N_DAYS = (END - START).days + 1


def read_players():
    history = read_characters(SERVERS, START, END)
    history.print_completeness_report()
    players = history.all_players()
    n_players = len(players)
    print(f'{n_players} players recognized')
    return players


if __name__ == '__main__':
    players = read_players()

    first_birth_trace = go.Histogram(x=[p.first_birth() for p in players], name='First Seen')
    last_death_trace = go.Histogram(x=[p.last_death() for p in players], name='Last Seen')

    title = f'Players Joining and Leaving from {START} to {END} on Servers {", ".join([str(s) for s in SERVERS])}'

    py.plot({'data': [first_birth_trace, last_death_trace], 'layout': {'title': title}})
