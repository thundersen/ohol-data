from datetime import datetime, timedelta

from logreader.ohol_character import OholCharacter
from tests.time_factories import hour

default_birth = datetime(2019, 1, 1)


def surviving_mom_with_daughter():
    sut = female()
    sut.add_kid(female(id='ABC'))
    return sut


def surviving_mom_with_only_boys():
    sut = female()
    sut.add_kid(male(id='DEF'))
    return sut


def surviving_mom_with_no_kids():
    sut = female()
    sut.add_kid(male(id='DEF'))
    return sut


def female(id='123', birth=default_birth, death=None):
    sut = OholCharacter(id)
    sut.birth = birth
    sut.death = (birth + timedelta(minutes=60)) if death is None and birth is not None else death
    sut.sex = 'F'
    return sut


def eve(id='123', birth=default_birth, death=None):
    sut = female(id, birth, death)
    sut.mark_as_eve()
    return sut


def male(id='123', birth=default_birth, death=None):
    sut = female(id, birth, death)
    sut.sex = 'M'
    return sut


def make_character(param):
    split = param.split()
    character = OholCharacter(split[0])
    character.sex = split[1]
    character.birth = hour(split[2])
    character.death = hour(split[3])
    return character
