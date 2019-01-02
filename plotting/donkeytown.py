from datetime import date

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters
from timeutils.timeutils import date_range

SERVERS = [1]

START = date(2018, 12, 25)

END = date(2019, 1, 1)

if __name__ == '__main__':

    history = read_characters(SERVERS, START, END)

    characters = history.complete_characters()

    matrix = [[
        c.birth_coordinates.x,
        c.birth_coordinates.y,
        c.birth_coordinates.distance_from_zero(),
        (c.birth_coordinates.distance_from_zero() > 100000),
        c.birth.date(),
        c.birth
    ] for c in characters]

    df_all = pd.DataFrame.from_records(matrix, columns=['x', 'y', 'distance_from_zero', 'is_crazy_far', 'day', 'birth'])

    print(df_all.describe())

    df = df_all[df_all['is_crazy_far'] == False]

    p90 = df['distance_from_zero'].quantile(0.9)

    df['is_donkeytown'] = df['distance_from_zero'] > p90

    print(df.describe())

    data = go.Histogram(y=df['is_donkeytown'])

    maps = []
    for day in date_range(START, END):
        df_day = df[df['day'] == day]

        maps.append(go.Scatter(
            x=df_day['x'],
            y=df_day['y'],
            name=str(day),
            mode='markers',
            opacity=.8
        ))

    outliers = df_all[df_all['is_crazy_far'] == True]
    outliers = outliers[['x', 'y', 'birth']]

    print(outliers)

    py.plot({'data': maps, 'layout': {'title': 'Birth Coordinates on Server ' + str(SERVERS[0])}}, filename='donkeytown.html')
