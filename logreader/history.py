from logreader.lineage import Lineage
from logreader.ohol_character import OholCharacter


class History:
    def __init__(self):
        self.character_data = {}
        self.lineage_data = {}
        self.characters = {}
        self.lineages = {}
        self.incomplete = {}

    def record_name(self, character_id, name):
        character = self._find_or_create_character(character_id)
        character['name'] = name

    def record_birth(self, character_id, at, mom_id, sex):
        character = self._find_or_create_character(character_id)

        character['birth'] = at
        character['sex'] = sex

        self._record_relations(character, mom_id)

    def _find_or_create_character(self, character_id):
        if character_id not in self.character_data:
            self.character_data[character_id] = {
                'id': character_id,
                'kids': []
            }
        return self.character_data[character_id]

    def _record_relations(self, character, mom_id):
        if mom_id is None:
            character['is_eve'] = True
            self.lineage_data[character['id']] = {'eve': character}
        elif mom_id in self.character_data:
            mom = self.character_data[mom_id]
            mom['kids'].append(character)
        else:
            print('ERROR: unknown mom %s for character %s born at %s' % (mom_id, character['id'], character['birth']))

    def record_death(self, character_id, timestamp):
        character = self._find_or_create_character(character_id)
        character['death'] = timestamp

    def print_completeness_report(self):
        total = len(self.character_data)

        n_incomplete = len(self.incomplete)

        percent_incomplete = float(n_incomplete) / total * 100

        print("%s/%s = %.2f%% incomplete" % (n_incomplete, total, percent_incomplete))

    def complete_characters(self):
        return self.characters.values()

    def all_lineages(self):
        return self.lineages.values()

    def lineage(self, lineage_id):
        return self.lineages[lineage_id]

    def character(self, character_id):
        return self.characters[character_id]

    def write_all(self):
        for character_id, data in self.character_data.items():
            try:
                self.characters[character_id] = OholCharacter(**data)
            except KeyError:
                self.incomplete[character_id] = data

        for eve_id, data in self.lineage_data.items():
            if eve_id in self.characters:
                self.lineages[eve_id] = Lineage(self.characters[eve_id])
