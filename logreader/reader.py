from datetime import datetime

from logreader.history import History


def read_complete_characters(names_file, lifelog_file):
    history = read_characters(names_file, lifelog_file)

    history.print_completeness_report()

    return history.complete_characters()


def read_characters(names_file, lifelog_file):
    history = History()

    with open(names_file, "r") as file:
        for line in file:
            split = line.split()
            character_id = split[0]
            name = " ".join(split[1:])
            history.record_name(character_id, name)

    with open(lifelog_file, "r") as file:
        for line in file:
            split = line.split()

            log_type = split[0]
            timestamp = datetime.utcfromtimestamp(int(split[1]))
            character_id = split[2]

            if log_type == 'B':

                parent = split[6]
                mom_id = None if parent == 'noParent' else parent.split('=')[1]
                sex = split[4]

                history.record_birth(character_id, timestamp, mom_id, sex)
            elif log_type == 'D':
                history.record_death(character_id, timestamp)
            else:
                print('ERROR: unknown log type in ' + line)

    history.write_all()

    return history

