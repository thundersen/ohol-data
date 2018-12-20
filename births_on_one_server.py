#!env/bin/python3

from datetime import datetime, timedelta
import calendar
import pandas as pd

LOG = 'test_data/2018_12December_18_Tuesday.txt'

NAMES = 'test_data/2018_12December_18_Tuesday_names.txt'


def normalized_minute(timestamp):
    if timestamp.second < 30:
        return timestamp - timedelta(seconds=timestamp.second)
    else:
        return timestamp + timedelta(seconds=60-timestamp.second)


class Character:
    def __init__(self, id, name='[UNKNOWN]'):
        self.sex = None
        self.death = None
        self.birth = None
        self.id = id
        self.name = name

    def __str__(self):
        return self.id + " | " + self.name + " | " + str(self.birth) + "-" + str(self.death)

    def is_complete(self):
        return self.birth is not None and self.death is not None

    def get_fertile_mom_minutes(self):
        if self.sex is not 'F' or not self.is_complete():
            return []
        return minute_range(normalized_minute(self.birth), normalized_minute(self.death))


character = {}

with open(NAMES, "r") as file:
    for line in file:
        split = line.split()
        character[split[0]] = Character(split[0], " ".join(split[1:]))

with open(LOG, "r") as file:
    for line in file:
        split = line.split()
        character_id = split[2]

        if character_id not in character:
            character[character_id] = Character(character_id)

        timestamp = datetime.utcfromtimestamp(int(split[1]))
        log_type = split[0]

        if log_type == 'B':
            character[character_id].birth = timestamp
            character[character_id].sex = split[4]
        elif log_type == 'D':
            character[character_id].death = timestamp
        else:
            print('ERROR: unknown log type in ' + line)

n_characters = len(character)
n_complete_characters = len([c for c in character.values() if c.is_complete()])

percent_complete = float(n_complete_characters) / n_characters * 100
print("%s/%s = %.2f%% complete" % (n_complete_characters, n_characters, percent_complete))


def minute_range(start, end_dt):
    res = []
    current = utc_date(start)
    end = utc_date(end_dt)
    while current < end:
        res.append(current)
        current += timedelta(minutes=1)
    return res


def utc_date(naive):
    return datetime.utcfromtimestamp(calendar.timegm((
        naive.year, naive.month, naive.day, naive.minute, naive.second, naive.microsecond)))


minutes = minute_range(datetime(2018, 12, 18), datetime(2018, 12, 19))

class Stats:
    def __init__(self):
        n_fertile_moms = 0
        n_births = 0


minute_stats = {}
for m in minutes:
    minute_stats[m] = Stats()


for character in character.values():
    print(character.get_fertile_mom_minutes())

def plot_births():
    global file
    births = []
    with open(LOG, "r") as file:
        for birth_line in [l for l in file if l.startswith('B')]:
            unix_time = int(birth_line.split()[1])
            time = datetime.utcfromtimestamp(unix_time)
            births.append((time, 1))
    print(len(births))
    df = pd.DataFrame.from_records(births, index='time', columns=['time', 'count'])
    df_sampled = df.resample("5T").sum().reset_index()
    # print(df.index)
    # scatter = go.Scatter(x=df_sampled.index, y=df_sampled['count'])
    # py.plot([scatter])


plot_births()
