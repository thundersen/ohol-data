#!env/bin/python3
import os
from datetime import date

import requests

from logreader.logfile_names import build_names, LOCAL_DIR

SERVERS = [1, 2, 3]

START_DATE = date(2018, 12, 18)
END_DATE = date(2018, 12, 18)

BASE_URL = 'http://onehouronelife.com/publicLifeLogData/'


def download_all():
    filenames = build_names(SERVERS, START_DATE, END_DATE)

    for f in filenames:
        download_to_disk(f)


def download_to_disk(file):

    print("downloading " + file)

    content = requests.get(BASE_URL + file, headers={'Accept': 'application/octet-stream'}).content

    subdir = file.split('/')[0]

    create_dir(f'{LOCAL_DIR}/{subdir}')

    with open(f'{LOCAL_DIR}/{file}', "wb") as file:
        file.write(content)


def create_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        print('Error: Creating directory. ' + directory)
        raise e


if __name__ == '__main__':
    download_all()
