from datetime import date
import csv
import zipfile
from zipfile import ZipFile

from logreader.reader import read_history

SERVERS = [1, 2, 3, 4, 5, 6, 7]
FROM_DATE = date(2018, 8, 1)
TO_DATE = date(2018, 12, 30)


def write_characters(history):
    character_lineages = {}
    for lineage in history.all_lineages():
        for c in lineage.characters():
            character_lineages[c.id] = lineage.id()

    column_names = [
        'lineage_eve_id', 'id', 'mom_id', 'name', 'sex', 'is_eve',
        'birth', 'death', 'fertility_start', 'fertility_end']

    rows = [[character_lineages[c.id] if c.id in character_lineages else None,
             c.id,
             c.mom_id,
             c.name,
             c.sex,
             c.is_eve,
             c.birth,
             c.death,
             c.fertility_start() if c.sex == 'F' else None,
             c.fertility_end() if c.sex == 'F' else None]
            for c in history.complete_characters()]

    write_csv('characters', column_names, rows)


def write_csv(name, column_names, rows):
    with open(name + '.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(column_names)
        writer.writerows(rows)


def write_lineages(history):
    column_names = [
        'eve_id', 'eve_birth', 'last_fertility_end', 'n_members']

    rows = [[l.id(), l.duration().start_datetime, l.duration().end_datetime, len(l.characters())]
            for l in history.all_lineages()]

    write_csv('lineages', column_names, rows)


if __name__ == '__main__':
    history = read_history(SERVERS, FROM_DATE, TO_DATE)

    write_characters(history)
    write_lineages(history)

    zip_name = f'{"_".join([str(s) for s in SERVERS])}_{FROM_DATE}-{TO_DATE}.zip'

    with ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write('lineages.csv')
        myzip.write('characters.csv')
