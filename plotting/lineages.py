from datetime import date

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_history

SERVERS = [1]
FROM_DATE = date(2018, 12, 28)
TO_DATE = date(2018, 12, 28)

# SERVERS = [1]
# FROM_DATE = date(2018, 12, 28)
# TO_DATE = date(2018, 12, 28)

MIN_LINEAGE_LENGTH_SECONDS = 3600


def to_hours(duration):
    return float(duration.get_timedelta_second()) / 3600


def make_lineage_trace(lineages):
    filtered_lineages = [
        l for l in lineages
        if l.duration().get_timedelta_second() >= MIN_LINEAGE_LENGTH_SECONDS]

    print(f'plotting {len(filtered_lineages)} lineages')

    matrix = [[l.id(), l.duration().end_datetime, to_hours(l.duration())] for l in filtered_lineages]

    df = pd.DataFrame.from_records(matrix, index='id', columns=['id', 'death', 'lifespan_hours'])

    return go.Scatter(
        x=df['death'],
        y=df['lifespan_hours'],
        mode='markers',
        name='lineages',
        yaxis='y2',
        line=dict(color='rgb(0, 170, 255)')
    )


def make_player_trace(player_counts_dict):
    matrix = [[minute, count['total']] for minute, count in player_counts_dict.items()]

    df = pd.DataFrame.from_records(matrix, index='time', columns=['time', 'count'])

    df_avg = df.resample("H").mean().reset_index()

    return go.Scatter(
        x=df_avg['time'],
        y=df_avg['count'],
        name='players',
        line=dict(color='rgb(40, 255, 100)'),
        opacity=0.5
    )


if __name__ == '__main__':
    history = read_history(SERVERS, FROM_DATE, TO_DATE)

    lineage_trace = make_lineage_trace(history.all_lineages())

    player_trace = make_player_trace(history.total_player_counts())

    layout = dict(
        title='Lineages on Servers %s' % (", ".join(str(s) for s in SERVERS)),
        yaxis=dict(
            title='players',
            side='right'
        ),
        yaxis2=dict(
            title='lineage duration in hours',
            overlaying='y'
        ),
        xaxis=dict(
            title='time last mother became infertile'
        )
    )

    py.plot({'data': [player_trace, lineage_trace], 'layout': layout})
