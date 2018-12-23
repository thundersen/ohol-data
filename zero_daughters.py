from datetime import datetime

from logreader.reader import read_characters

LOG = 'test_data/server01/2018_12December_18_Tuesday.txt'

NAMES = 'test_data/server01/2018_12December_18_Tuesday_names.txt'

START = datetime(2018, 12, 18)

END = datetime(2018, 12, 19)


if __name__ == '__main__':
    characters = read_characters(NAMES, LOG)

    for c in characters.values():
        c.read_kids(characters)

    zero_daughters = [x for x in characters.values() if x.is_zero_girl_mom()]

    with_daughters = [x for x in characters.values() if x.is_mom_with_girls()]

    print(len(zero_daughters))
