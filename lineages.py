from datetime import date

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters

SERVER = 1
DATE = date(2018, 12, 28)


def to_hours(duration):
    delta = (duration.end_datetime - duration.start_datetime)

    return delta.days * 24 + float(delta.seconds) / 3600


def make_lineage_plot(history):
    lineages = history.all_lineages()
    matrix = [[l.id(), l.duration().end_datetime, to_hours(l.duration())] for l in lineages]
    df = pd.DataFrame.from_records(matrix, index='id', columns=['id', 'death', 'lifespan_hours'])
    return go.Scatter(x=df['death'], y=df['lifespan_hours'], mode='markers', name='ending lineages')


if __name__ == '__main__':

    history = read_characters(SERVER, DATE)

    lineage_plot = make_lineage_plot(history)

    layout = dict(
        title='Lineages on Server %s at %s' % (SERVER, DATE),
        yaxis=dict(
            title='lineage duration in hours'
        ),
        xaxis=dict(
            title='time the lineage ended (last mom becomes infertile)'
        )
    )

    py.plot({'data': [lineage_plot], 'layout': layout })
