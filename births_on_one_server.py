#!env/bin/python3

from datetime import datetime

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from OholCharacter import OholCharacter
from timeutils.timeutils import round_minute_range, round_minute

LOG = 'test_data/2018_12December_18_Tuesday.txt'

NAMES = 'test_data/2018_12December_18_Tuesday_names.txt'

characters = {}

with open(NAMES, "r") as file:
    for line in file:
        split = line.split()
        characters[split[0]] = OholCharacter(split[0], " ".join(split[1:]))

with open(LOG, "r") as file:
    for line in file:
        split = line.split()
        character_id = split[2]

        if character_id not in characters:
            characters[character_id] = OholCharacter(character_id)

        timestamp = datetime.utcfromtimestamp(int(split[1]))
        log_type = split[0]

        if log_type == 'B':
            characters[character_id].birth = timestamp
            characters[character_id].sex = split[4]
        elif log_type == 'D':
            characters[character_id].death = timestamp
        else:
            print('ERROR: unknown log type in ' + line)

n_characters = len(characters)

incomplete_characters = [c for c in characters.values() if not c.is_complete()]

n_incomplete_characters = len(incomplete_characters)

percent_incomplete = float(n_incomplete_characters) / n_characters * 100

print("%s/%s = %.2f%% incomplete" % (n_incomplete_characters, n_characters, percent_incomplete))

for character_id in [c.id for c in incomplete_characters]:
    del characters[character_id]

minutes = round_minute_range(datetime(2018, 12, 18), datetime(2018, 12, 19))


class Stats:
    def __init__(self):
        self.n_fertile_moms = 0
        self.n_births = 0

    def births_per_mom(self):
        return 0 if self.n_fertile_moms == 0 else float(self.n_births) / self.n_fertile_moms


minute_stats = {}
for m in minutes:
    minute_stats[m] = Stats()

for character in characters.values():

    minute_stats[round_minute(character.birth)].n_births += 1

    for minute in character.get_fertile_mom_minutes():
        minute_stats[minute].n_fertile_moms += 1

matrix = [[m, stat.n_births, stat.n_fertile_moms, stat.births_per_mom()]
          for m, stat in minute_stats.items() if m.hour >= 12]

df = pd.DataFrame.from_records(matrix, index='time', columns=['time', 'births', 'fertile_moms', 'births_per_mom'])

df_sum = df.resample("5T").sum().reset_index()
df_avg = df.resample("5T").mean().reset_index()

births = go.Scatter(x=df_avg['time'], y=df_avg['births'], name='births per minute')
mothers = go.Scatter(x=df_avg['time'], y=df_avg['fertile_moms'], name='fertile moms')
bpm = go.Scatter(x=df_avg['time'], y=df_avg['births_per_mom'], name='births per mom per minute')

interesting_mom = characters['805831']

print(interesting_mom)

fertility_minutes = round_minute_range(
    interesting_mom.fertility_start(),
    interesting_mom.fertility_end())

avg_kids_during_fertility = sum(
    [minute_stats[minute].births_per_mom() for minute in minute_stats if minute in fertility_minutes]
)

layout = dict(
    title=interesting_mom.name + "'s Misfortune",
    shapes=[
        dict(
            type='rect',
            xref='x',
            yref='paper',
            x0=interesting_mom.fertility_start(),
            y0=0,
            x1=interesting_mom.fertility_end(),
            y1=1,
            fillcolor='#d3d3d3',
            opacity=0.4,
            line={
                'width': 0,
            }
        )
    ]
)

py.plot({
    'data': [
        births,
        mothers,
        bpm
    ],
    'layout': layout})

