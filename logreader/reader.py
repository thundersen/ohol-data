import os
from datetime import datetime

from logreader.coordinates import Coordinates
from logreader.history import History
from logreader.logfile_names import build_local_filenames_for_server_and_day
from timeutils.timeutils import date_range


def read_characters(servers, from_date, to_date):
    history = History()

    for server in servers:
        for day in date_range(from_date, to_date):
            read_for_server_at_date(history, server, day)

    history.write_all()

    return history


def read_for_server_at_date(history, server_no, day):
    files = build_local_filenames_for_server_and_day(server_no, day)

    has_players = _record_players_from_names(files['names'], history, server_no)

    if not has_players:
        return

    _record_events_from_log(files['log'], history, server_no)


def _has_players(open_file):
    for i, line in enumerate(open_file):
        if i == 1:
            return '404 Not Found' not in line


def _read(history, line, reading_func, filename, server_no):
    try:
        reading_func(history, line, server_no)
    except (IndexError, ValueError):
        print(f'ERROR reading data from {filename}:\n>>> {line}')


def _record_players_from_names(filename, history, server_no):
    if not os.path.exists(filename):
        print('WARNING: file not found ' + filename)
        return

    with open(filename, "r") as file:

        if not _has_players(file):
            return False

        for line in file:
            _read(history, line, _record_names_line, filename, server_no)

    return True


def _record_events_from_log(filename, history, server_no):
    if not os.path.exists(filename):
        print('WARNING: file not found ' + filename)
        return

    with open(filename, "r") as file:
        for line in file:
            _read(history, line, _record_log_line, filename, server_no)


def _server_specific_id_from(raw_id, server_no):
    return f'{server_no}_{raw_id}'


def _coordinates_from(coordinates_string):
    split = coordinates_string.strip('()').split(',')
    return Coordinates(int(split[0]), int(split[1]))


def _record_log_line(history, line, server_no):
    split = line.split()
    log_type = split[0]
    timestamp = datetime.utcfromtimestamp(int(split[1]))
    character_id = _server_specific_id_from(split[2], server_no)

    if log_type == 'B':

        parent = split[6]
        mom_id = None if parent == 'noParent' else _server_specific_id_from(parent.split('=')[1], server_no)
        sex = split[4]
        coordinates = _coordinates_from(split[5])

        history.record_birth(character_id, timestamp, mom_id, sex, coordinates)
        _record_player_count(history, split[7], timestamp, server_no)
    elif log_type == 'D':
        history.record_death(character_id, timestamp)
        _record_player_count(history, split[8], timestamp, server_no)
    else:
        print('ERROR: unknown log type in ' + line)


def _record_names_line(history, line, server_no):
    split = line.split()
    character_id = _server_specific_id_from(split[0], server_no)
    name = " ".join(split[1:])
    history.record_name(character_id, name)


def _record_player_count(history, count_element, timestamp, server_no):
    player_count = int(count_element.split('=')[1])
    history.record_player_count(timestamp, player_count, server_no)
