from datetime import datetime

from logreader.reader import read_characters

LOG = 'lifelogs/server01/2018_12December_18_Tuesday.txt'

NAMES = 'lifelogs/server01/2018_12December_18_Tuesday_names.txt'

START = datetime(2018, 12, 18)

END = datetime(2018, 12, 19)


if __name__ == '__main__':
    history = read_characters(NAMES, LOG)

    zero_daughters = [x for x in history.complete_characters() if x.is_zero_girl_mom()]

    with_daughters = [x for x in history.complete_characters() if x.is_mom_with_girls()]

    survivor_mums = [x for x in history.complete_characters() if x.is_surviving_mom()]

    print(len(zero_daughters))
