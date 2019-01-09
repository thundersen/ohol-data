#!env/bin/python3

from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_history
from timeutils.timeutils import round_minute_range, round_minute

SERVER = 3

START = datetime(2018, 12, 18)

END = datetime(2018, 12, 19)

INTERESTING_MOM_ID = '805831'


class Stats:
    def __init__(self):
        self.n_fertile_moms = 0
        self.n_births = 0

    def births_per_mom(self):
        return 0 if self.n_fertile_moms == 0 else float(self.n_births) / self.n_fertile_moms


def create_stats_per_minute(history, start, end):

    result = {}

    for m in round_minute_range(start, end):
        result[m] = Stats()

    for character in history.complete_characters():

        if not history.is_orphan(character.id):
            result[round_minute(character.birth)].n_births += 1

        for minute in character.fertile_mom_minutes():
            result[minute].n_fertile_moms += 1

    return result


def arrange_plot_data(minute_stats, player_counts_per_minute):

    matrix = [[
        m,
        stat.n_births,
        stat.n_fertile_moms,
        stat.births_per_mom(),
        player_counts_per_minute[m] if m in player_counts_per_minute else None
    ] for m, stat in minute_stats.items()]

    df = pd.DataFrame.from_records(
        matrix, index='time', columns=['time', 'births', 'fertile_moms', 'births_per_mom', 'player_count'])

    df_avg = df.resample("5T").mean().reset_index()

    player_count = go.Scatter(x=df_avg['time'], y=df_avg['player_count'], name='# players')
    mothers = go.Scatter(x=df_avg['time'], y=df_avg['fertile_moms'], name='# fertile moms')
    # births = go.Scatter(x=df_avg['time'], y=df_avg['births'], name='births per minute', yaxis='y2')
    bpm = go.Scatter(x=df_avg['time'], y=df_avg['births_per_mom'], name='births per mom per minute', yaxis='y2')

    return [player_count, mothers, bpm]


def print_expected_kids(interesting_mom):
    fertility_minutes = round_minute_range(
        interesting_mom.fertility_start(),
        interesting_mom.fertility_end())

    births_per_mom = [minute_stats[minute].births_per_mom() for minute in minute_stats if minute in fertility_minutes]

    expected_kids = sum(births_per_mom)

    print("Expected number of kids during fertility period: %s" % expected_kids)


def create_plot(mom, data):
    layout = dict(
        title=mom.name + "'s Misfortune",
        shapes=[
            dict(
                type='rect',
                xref='x',
                yref='paper',
                x0=mom.fertility_start(),
                y0=0,
                x1=mom.fertility_end(),
                y1=1,
                fillcolor='#d3d3d3',
                opacity=0.4,
                line={
                    'width': 0,
                }
            )
        ]
    )
    py.plot({'data': data, 'layout': layout})


if __name__ == '__main__':

    history = read_history([SERVER], START, START)

    minute_stats = create_stats_per_minute(history, START, END)

    plot_data = arrange_plot_data(minute_stats, history.total_player_counts())

    layout = dict(
        title='Births on Server %s' % SERVER,
        yaxis=dict(
            title='# characters'
        ),
        yaxis2=dict(
            title='births per minute',
            overlaying='y',
            side='right'
        )
    )
    py.plot({'data': plot_data, 'layout': layout})

#    interesting_mom = characters[INTERESTING_MOM_ID]

#    print(interesting_mom)

#    print_expected_kids(interesting_mom)
#    create_plot(interesting_mom, plot_data)


