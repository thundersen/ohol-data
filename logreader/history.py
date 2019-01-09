from datetime import timedelta

from logreader.lineage import Lineage
from logreader.character import Character
from logreader.player import Player
from logreader.player_count_tracker import PlayerCountTracker


class History:
    def __init__(self):
        self._character_data = {}
        self._lineage_data = {}
        self._characters = {}
        self._lineages = {}
        self._players = {}
        self._incomplete = {}
        self._orphans = []
        self._count_tracker = PlayerCountTracker()
        self._murder_victims = {}

    def record_name(self, character_id, name):
        character = self._find_or_create_character(character_id, 'name', name)
        character['name'] = name

    def record_birth(self, character_id, at, mom_id, sex, coordinates, player):
        character = self._find_or_create_character(character_id, 'birth', at)

        character['birth'] = at
        character['birth_coordinates'] = coordinates
        character['sex'] = sex
        character['mom_id'] = mom_id
        character['player'] = player

        if mom_id is None:
            character['is_eve'] = True
            self._lineage_data[character['id']] = {'eve': character}
        else:
            self._record_relations(character, mom_id)

    def record_death(self, character_id, timestamp, coordinates, murderer_id):
        character = self._find_or_create_character(character_id, 'death', timestamp)
        character['death'] = timestamp
        character['death_coordinates'] = coordinates
        character['murderer_id'] = murderer_id

        if murderer_id is not None:
            self._record_murder(character_id, murderer_id)

    def _record_murder(self, character_id, murderer_id):
        if murderer_id not in self._murder_victims:
            self._murder_victims[murderer_id] = [character_id]
        else:
            self._murder_victims[murderer_id].append(character_id)

    def _find_or_create_character(self, character_id, new_key, new_value):

        if character_id not in self._character_data:
            self._character_data[character_id] = {
                'id': character_id,
                'kids_data': []
            }
            return self._character_data[character_id]

        character = self._character_data[character_id]

        if new_key not in character:
            return character

        new_id = character_id + 'd'
        print(f'ERROR: duplicate id {character_id} - first birth: {character[new_key]}, second: {new_value}')
        print(f'       assigning new ID {new_id}')

        return self._find_or_create_character(new_id, new_key, new_value)

    def _record_relations(self, character, mom_id):

        if mom_id in self._character_data:
            mom = self._character_data[mom_id]
            if ('death' in mom and mom['death'] < character['birth']) or \
                    ('birth' in mom and character['birth'] - mom['birth'] > timedelta(minutes=40)):
                print(f'WARNING: implausible mom {mom_id} {mom["birth"]}-{mom["death"]} '
                      f'for {character["id"]}. Assuming duplicate ID')
                self._record_relations(character, mom_id + 'd')
                return

            mom['kids_data'].append(character)
        else:
            self._orphans.append(character['id'])
            print('ERROR: unknown mom %s for character %s born at %s' % (mom_id, character['id'], character['birth']))

    def record_player_count(self, timestamp, count, server_no):
        self._count_tracker.record_player_count(timestamp, count, server_no)

    def print_completeness_report(self):
        total = len(self._character_data)

        n_incomplete = len(self._incomplete)

        percent_incomplete = float(n_incomplete) / total * 100

        print("%s/%s = %.2f%% incomplete" % (n_incomplete, total, percent_incomplete))

    def complete_characters(self):
        return self._characters.values()

    def all_lineages(self):
        return self._lineages.values()

    def all_players(self):
        return self._players.values()

    def lineage(self, lineage_id):
        return self._lineages[lineage_id]

    def character(self, character_id):
        return self._characters[character_id]

    def is_orphan(self, character_id):
        return character_id in self._orphans

    def total_player_counts(self):
        return self._count_tracker.player_counts()

    def write_all(self):
        self._write_characters()
        self._write_lineages()
        self._write_players()
        self._count_tracker.write_player_counts()

    def _write_lineages(self):
        for eve_id, data in self._lineage_data.items():
            if eve_id in self._characters:
                self._lineages[eve_id] = Lineage(self._characters[eve_id])

    def _write_players(self):
        for character_id, character in self._characters.items():
            if character.player not in self._players:
                self._players[character.player] = Player(character.player)
            self._players[character.player].add_character(character)

    def _write_characters(self):
        for character_id, data in self._reversed_character_data_items():

            kids = [k for k in [self._try_find_kid(kid_data['id']) for kid_data in data['kids_data']] if k is not None]

            data['murder_victims'] = self._murder_victims[character_id] if character_id in self._murder_victims else []

            try:
                self._characters[character_id] = Character(kids=kids, **data)
            except KeyError as e:
                self._write_incomplete(character_id, data, e)

    def _write_incomplete(self, character_id, data, error):
        birth_str = data['birth'] if 'birth' in data else '[UNKNOWN BIRTH]'
        death_str = data['death'] if 'death' in data else '[UNKNOWN DEATH]'
        name_str = data['name'] if 'name' in data else '[UNKNOWN NAME]'
        print(f'ERROR: missing data for {name_str} {character_id} {birth_str}-{death_str}: {error}')
        self._incomplete[character_id] = data

    def _try_find_kid(self, kid_id):
        try:
            return self._characters[kid_id]
        except KeyError:
            reason = 'incomplete' if kid_id in self._incomplete else 'unknown'

            print(f'WARNING: ignoring {reason} kid {kid_id}')

    def _reversed_character_data_items(self):
        """
        assuming that kids have been entered *after* mothers, reversing ensures that kids
        are processed *before* mothers.
        hence there are already Character instances for kids, which can be referenced by mothers.
        referencing avoids having to create additional instances for kids inside of mothers recursively.
        """
        return sorted(list(self._character_data.items()), key=lambda x: x[0].lower(), reverse=True)
