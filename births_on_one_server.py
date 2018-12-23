#!env/bin/python3

from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_complete_characters
from timeutils.timeutils import round_minute_range, round_minute

LOG = 'lifelogs/server01/2018_12December_18_Tuesday.txt'

NAMES = 'lifelogs/server01/2018_12December_18_Tuesday_names.txt'

START = datetime(2018, 12, 18)

END = datetime(2018, 12, 19)

INTERESTING_MOM_ID = '805831'


class Stats:
    def __init__(self):
        self.n_fertile_moms = 0
        self.n_births = 0

    def births_per_mom(self):
        return 0 if self.n_fertile_moms == 0 else float(self.n_births) / self.n_fertile_moms


def create_stats_per_minute(characters, start, end):

    result = {}

    for m in round_minute_range(start, end):
        result[m] = Stats()

    for character in characters.values():

        result[round_minute(character.birth)].n_births += 1

        for minute in character.fertile_mom_minutes():
            result[minute].n_fertile_moms += 1

    return result


def arrange_plot_data(minute_stats):

    matrix = [[m, stat.n_births, stat.n_fertile_moms, stat.births_per_mom()]
              for m, stat in minute_stats.items()]

    df = pd.DataFrame.from_records(matrix, index='time', columns=['time', 'births', 'fertile_moms', 'births_per_mom'])

    df_avg = df.resample("5T").mean().reset_index()

    births = go.Scatter(x=df_avg['time'], y=df_avg['births'], name='births per minute')
    mothers = go.Scatter(x=df_avg['time'], y=df_avg['fertile_moms'], name='fertile moms')
    bpm = go.Scatter(x=df_avg['time'], y=df_avg['births_per_mom'], name='births per mom per minute')

    return [births, mothers, bpm]


def print_expected_kids(interesting_mom):
    fertility_minutes = round_minute_range(
        interesting_mom.fertility_start(),
        interesting_mom.fertility_end())

    births_per_mom = [minute_stats[minute].births_per_mom() for minute in minute_stats if minute in fertility_minutes]

    expexted_kids = sum(births_per_mom)

    print("Expected number of kids during fertility period: %s" % expexted_kids)


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
    characters = read_complete_characters(NAMES, LOG)

    minute_stats = create_stats_per_minute(characters, START, END)

    plot_data = arrange_plot_data(minute_stats)

#    interesting_mom = characters[INTERESTING_MOM_ID]

#    print(interesting_mom)

#    print_expected_kids(interesting_mom)

#    create_plot(interesting_mom, plot_data)

    py.plot(plot_data)
