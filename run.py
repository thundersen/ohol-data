#!env/bin/python3
import datetime
import sched

import requests


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


def write(data):
    data_line = ';'.join(data)
    with open("OholPlayersByServer.csv", "a") as file:
        file.write(data_line + '\n')
    print(data_line)


def get_current_player_counts():
    data = fetch()
    write(data)


def periodic(scheduler, interval, action):
    scheduler.enter(interval, 1, periodic, (scheduler, interval, action))
    action()


if __name__ == '__main__':
    s = sched.scheduler()
    periodic(s, 5 * 60, get_current_player_counts)
    s.run()
