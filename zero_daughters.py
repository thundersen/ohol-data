from datetime import date

from logreader.reader import read_characters

SERVER = 1
DATE = date(2018, 12, 18)


if __name__ == '__main__':
    history = read_characters([SERVER], DATE, DATE)

    zero_daughters = [x for x in history.complete_characters() if x.is_zero_girl_mom()]

    with_daughters = [x for x in history.complete_characters() if x.is_mom_with_girls()]

    survivor_mums = [x for x in history.complete_characters() if x.is_surviving_mom()]

    print(len(zero_daughters))
