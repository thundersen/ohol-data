
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters


LOG = 'lifelogs/server02/2018_12December_18_Tuesday.txt'

NAMES = 'lifelogs/server02/2018_12December_18_Tuesday_names.txt'


def to_hours(duration):
    delta = (duration.end_datetime - duration.start_datetime)

    return delta.days * 24 + float(delta.seconds) / 3600


def make_lineage_plot(history):
    lineages = history.all_lineages()
    matrix = [[l.id(), l.duration().end_datetime, to_hours(l.duration())] for l in lineages]
    df = pd.DataFrame.from_records(matrix, index='id', columns=['id', 'death', 'lifespan_hours'])
    return go.Scatter(x=df['death'], y=df['lifespan_hours'], mode='markers', name='ending lineages')


if __name__ == '__main__':
    history = read_characters(NAMES, LOG)

    lineage_plot = make_lineage_plot(history)

    py.plot([lineage_plot])
