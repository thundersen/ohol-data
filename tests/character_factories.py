from datetime import datetime, timedelta

from logreader.character import Character, UNKNOWN_NAME
from logreader.coordinates import Coordinates
from tests.time_factories import hour

default_birth = datetime(2019, 1, 1)


def surviving_mom_with_daughter():
    sut = female()
    sut.kids.append(female(id='ABC'))
    return sut


def surviving_mom_with_only_boys():
    sut = female()
    sut.kids.append(male(id='DEF'))
    return sut


def surviving_mom_with_no_kids():
    sut = female()
    sut.kids.append(male(id='DEF'))
    return sut


def female(id='123', birth=default_birth, death=None, is_eve=False, name=UNKNOWN_NAME):
    data = {
        'id': id,
        'name': name,
        'mom_id': None,
        'is_eve': is_eve,
        'sex': 'F',
        'player': '[SOMEONE]',
        'birth': birth,
        'birth_coordinates': Coordinates(0, 0),
        'death': (birth + timedelta(minutes=60)) if death is None and birth is not None else death,
        'death_coordinates': Coordinates(0, 0),
        'murderer_id': None,
        'murder_victims': []
    }
    return Character(kids=[], **data)


def eve(id='123', birth=default_birth, death=None, name=UNKNOWN_NAME):
    sut = female(id, birth, death, name=name)
    sut.is_eve = True
    return sut


def male(id='123', birth=default_birth, death=None):
    sut = female(id, birth, death)
    sut.sex = 'M'
    return sut


def make_character(param):
    split = param.split()
    data = {
        'id': split[0],
        'sex': split[1],
        'birth': hour(split[2]),
        'death': hour(split[3])
    }
    return Character(**data)
