from datetime import datetime

from logreader.ohol_character import OholCharacter


def read_complete_characters(names_file, lifelog_file):
    characters = read_characters(names_file, lifelog_file)

    print_completeness_report(characters)

    delete_incomplete_characters(characters)

    return characters


def read_characters(names_file, lifelog_file):
    characters = {}

    with open(names_file, "r") as file:
        for line in file:
            split = line.split()
            characters[split[0]] = OholCharacter(split[0], " ".join(split[1:]))

    with open(lifelog_file, "r") as file:
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

    return characters


def print_completeness_report(characters):
    n_characters = len(characters)

    n_incomplete_characters = len(incomplete_characters_from(characters))

    percent_incomplete = float(n_incomplete_characters) / n_characters * 100

    print("%s/%s = %.2f%% incomplete" % (n_incomplete_characters, n_characters, percent_incomplete))


def incomplete_characters_from(characters):
    return [c for c in characters.values() if not c.is_complete()]


def delete_incomplete_characters(characters):
    for character_id in [c.id for c in incomplete_characters_from(characters)]:
        del characters[character_id]
