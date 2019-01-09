from datetime import date, datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
from logreader.reader import read_history
from timeutils.timeutils import round_minute_range

SERVERS = [1,2,3]

START = date(2018, 12, 14)

END = date(2018, 12, 28)


def make_player_trace(player_counts_dict):
    matrix = [[minute, count] for minute, count in player_counts_dict.items()]

    df = pd.DataFrame.from_records(matrix, index='time', columns=['time', 'count'])

    df_avg = df.resample("H").mean().reset_index()

    return go.Scatter(
        x=df_avg['time'],
        y=df_avg['count'],
        name='players',
        line=dict(color='rgb(40, 255, 100)'),
        opacity=0.5
    )


class Stats:
    def __init__(self):
        self.n_fertile_moms = 0
        self.ratio_fertile_moms = 0
        self.n_players = None


def create_stats_per_minute(history, start, end):

    result = {}
    start_minute = datetime.combine(start, datetime.min.time())
    end_minute = datetime.combine(end + timedelta(days=1), datetime.min.time())

    for m in round_minute_range(start_minute, end_minute):
        result[m] = Stats()

    for character in history.complete_characters():

        for minute in character.fertile_mom_minutes():
            result[minute].n_fertile_moms += 1

    for minute, counts in history.total_player_counts().items():
        available_server_counts = [int(k[-2:]) for k in counts.keys() if k != 'total']
        if available_server_counts == SERVERS:
            result[minute].n_players = counts['total']

    return result


def arrange_plot_data(minute_stats):

    matrix = [[
        m,
        stat.n_fertile_moms,
        (float(stat.n_fertile_moms) / stat.n_players) if stat.n_players else None,
        stat.n_players if stat.n_players else None
    ] for m, stat in minute_stats.items()]

    df = pd.DataFrame.from_records(
        matrix, index='time', columns=['time', 'fertile_moms', 'ratio_fertile_moms', 'player_count'])

    print(df.describe())

    df_avg = df.resample("5T").mean().reset_index()

    mothers = go.Scatter(x=df_avg['time'], y=df_avg['fertile_moms'], name='# fertile moms')
    ratio = go.Scatter(x=df_avg['time'], y=df_avg['ratio_fertile_moms'], name='ratio fertile moms', yaxis='y2')
    player_count = go.Scatter(x=df_avg['time'], y=df_avg['player_count'], name='# players')

    return [mothers, ratio, player_count]


if __name__ == '__main__':

    history = read_history(SERVERS, START, END)

    minute_stats = create_stats_per_minute(history, START, END)

    plot_data = arrange_plot_data(minute_stats)

    layout = dict(
        title='Fertile mothers on servers %s' % (", ".join(str(s) for s in SERVERS)),
        yaxis=dict(
            title='# characters'
        ),
        yaxis2=dict(
            title='ratio',
            overlaying='y',
            side='right'
        )
    )
    py.plot({'data': plot_data, 'layout': layout})
