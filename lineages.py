from datetime import date

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters

SERVERS = [1, 2, 3]
FROM_DATE = date(2018, 11, 1)
TO_DATE = date(2018, 12, 28)

MIN_LINEAGE_LENGTH_SECONDS = 3600


def to_hours(duration):
    return float(duration.get_timedelta_second()) / 3600


def make_lineage_plot(lineages):

    filtered_lineages = [l for l in lineages if l.duration().get_timedelta_second() >= MIN_LINEAGE_LENGTH_SECONDS]

    print(f'plotting {len(filtered_lineages)} lineages')

    matrix = [[l.id(), l.duration().end_datetime, to_hours(l.duration())] for l in filtered_lineages]
    df = pd.DataFrame.from_records(matrix, index='id', columns=['id', 'death', 'lifespan_hours'])
    return go.Scatter(x=df['death'], y=df['lifespan_hours'], mode='markers', name='ending lineages')


if __name__ == '__main__':

    history = read_characters(SERVERS, FROM_DATE, TO_DATE)

    lineage_plot = make_lineage_plot(history.all_lineages())

    layout = dict(
        title='Lineages on Servers %s' % (", ".join(str(s) for s in SERVERS)),
        yaxis=dict(
            title='lineage duration in hours'
        ),
        xaxis=dict(
            title='time the lineage ended (last mom becomes infertile)'
        )
    )

    py.plot({'data': [lineage_plot], 'layout': layout })
