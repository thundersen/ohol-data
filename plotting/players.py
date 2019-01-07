from datetime import date, timedelta

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from logreader.reader import read_characters
from timeutils.timeutils import date_range

SERVERS = [1, 2, 3, 4, 5, 6, 7]

START = date(2018, 4, 1)

END = date(2018, 12, 31)

if __name__ == '__main__':
    history = read_characters(SERVERS, START, END)

    players = history.all_players()

    player_lives = [[p.player_id, len(p.characters)] for p in players]

    print(len(players))
