#!env/bin/python3
import datetime
import sched
import pandas as pd
import plotly.graph_objs as go
import requests
from plotly.offline import plot

CSV_FILE = 'OholPlayersByServer.csv'


def process_current_player_counts():
    data = fetch()
    write(data, CSV_FILE)
    draw(CSV_FILE)


def fetch():
    timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

    response = requests.get('http://onehouronelife.com/reflector/server.php?action=report')

    response.raise_for_status()

    raw = response.content

    player_counts = [parse_player_count(line) for line in parse_server_lines(raw)]

    return [timestamp] + player_counts


def parse_server_lines(raw):
    return [line for line in str(raw).split('<br><br>') if line.startswith('|--> server')]


def parse_player_count(server_line):
    return '' if server_line.endswith('OFFLINE') else server_line.split()[-3]


def write(data, filename):
    data_line = ';'.join(data)
    with open(filename, "a") as file:
        file.write(data_line + '\n')
    print(data_line)


def periodic(scheduler, interval, action):
    scheduler.enter(interval, 1, periodic, (scheduler, interval, action))
    action()


def draw(filename):
    servers = ['server%s' % (n + 1) for n in range(15)]

    df = pd.read_csv(filename, sep=';', names=['timestamp'] + servers)

    df['sum'] = df.apply(calculate_sum, axis=1)

    data = [plot_column(name, df) for name in servers + ['sum']]

    plot(data)


def calculate_sum(row):
    return sum(row[1:])


def plot_column(name, df):
    return go.Scatter(x=df.timestamp, y=df[name], name=name)


if __name__ == '__main__':
    s = sched.scheduler()
    periodic(s, 5 * 60, process_current_player_counts)
    s.run()
