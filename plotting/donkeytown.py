import zipfile
from zipfile import ZipFile
from datetime import date, timedelta

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_history
from timeutils.timeutils import date_range

SERVERS = [1]

START = date(2018, 12, 13)

END = date(2018, 12, 20)


def print_outliers(_df):
    outliers = _df[_df['is_crazy_far'] == True]
    outliers = outliers[['x', 'y', 'birth']]
    print(outliers)


def create_zip(html_filename):
    zipfile_name = html_filename.replace('.html', '.zip')
    with ZipFile(zipfile_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(html_filename)


def create_daily_traces(_df):
    result = []
    for day in date_range(START, END):
        df_day = _df[_df['day'] == day]

        result.append(go.Scatter(
            x=df_day['x'],
            y=df_day['y'],
            name=str(day),
            mode='markers',
            opacity=.8
        ))
    return result


def create_hourly_traces(_df):
    result = []
    for hour in range(0, 24):
        df_hour = _df[_df['birth_hour'] == hour]

        result.append(go.Scatter(
            x=df_hour['x'],
            y=df_hour['y'],
            name=str(hour),
            mode='markers',
            opacity=.8
        ))
    return result


if __name__ == '__main__':

    history = read_history(SERVERS, START, END)

    characters = history.complete_characters()

    matrix = [[
        c.birth_coordinates.x,
        c.birth_coordinates.y,
        c.birth_coordinates.distance_from_zero(),
        (c.birth_coordinates.distance_from_zero() > 100000),
        c.birth.date(),
        c.birth,
        c.birth.hour
    ] for c in characters if c.death - c.birth > timedelta(minutes=40)]

    df_all = pd.DataFrame.from_records(matrix, columns=['x', 'y', 'distance_from_zero', 'is_crazy_far', 'day', 'birth', 'birth_hour'])

    print(df_all.describe())

    print_outliers(df_all)

    df = df_all[df_all['is_crazy_far'] == False]

    print(df.describe())

    maps = create_daily_traces(df)

    # maps = create_hourly_traces(df)

    layout = {
        'title': 'Birth Coordinates on Server ' + str(SERVERS[0]),
        'yaxis': {'scaleanchor': 'x', 'scaleratio': 1}
    }

    filename = f'server{SERVERS[0]}_{START}-{END}.html'

    py.plot({'data': maps, 'layout': layout}, filename=filename)

    # create_zip(filename)
