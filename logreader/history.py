from logreader.lineage import Lineage
from logreader.character import Character
from logreader.player_count_tracker import PlayerCountTracker


class History:
    def __init__(self):
        self._character_data = {}
        self._lineage_data = {}
        self._characters = {}
        self._lineages = {}
        self._incomplete = {}
        self._orphans = []
        self._count_tracker = PlayerCountTracker()

    def record_name(self, character_id, name):
        character = self._find_or_create_character(character_id)
        character['name'] = name

    def record_birth(self, character_id, at, mom_id, sex, coordinates):
        character = self._find_or_create_character(character_id)

        character['birth'] = at
        character['birth_coordinates'] = coordinates
        character['sex'] = sex
        character['mom_id'] = mom_id

        self._record_relations(character, mom_id)

    def _find_or_create_character(self, character_id):
        if character_id not in self._character_data:
            self._character_data[character_id] = {
                'id': character_id,
                'kids_data': []
            }
        return self._character_data[character_id]

    def _record_relations(self, character, mom_id):
        if mom_id is None:
            character['is_eve'] = True
            self._lineage_data[character['id']] = {'eve': character}
        elif mom_id in self._character_data:
            mom = self._character_data[mom_id]
            mom['kids_data'].append(character)
        else:
            self._orphans.append(character['id'])
            print('ERROR: unknown mom %s for character %s born at %s' % (mom_id, character['id'], character['birth']))

    def record_death(self, character_id, timestamp):
        character = self._find_or_create_character(character_id)
        character['death'] = timestamp

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
        self._count_tracker.write_player_counts()

    def _write_lineages(self):
        for eve_id, data in self._lineage_data.items():
            if eve_id in self._characters:
                self._lineages[eve_id] = Lineage(self._characters[eve_id])

    def _write_characters(self):
        for character_id, data in self._reversed_character_data_items():
            try:
                kids = [self._characters[kid_id] for kid_id in [kid_data['id'] for kid_data in data['kids_data']]]
                self._characters[character_id] = Character(kids=kids, **data)
            except KeyError:
                self._incomplete[character_id] = data

    def _reversed_character_data_items(self):
        """
        assuming that kids have been entered *after* mothers, reversing ensures that kids
        are processed *before* mothers.
        hence there are already Character instances for kids, which can be referenced by mothers.
        referencing avoids having to create additional instances for kids inside of mothers recursively.
        """
        return sorted(list(self._character_data.items()), key=lambda x: x[0].lower(), reverse=True)
