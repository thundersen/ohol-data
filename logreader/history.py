from logreader.lineage import Lineage
from logreader.ohol_character import OholCharacter


class History:
    def __init__(self):
        self.characters = {}
        self.lineages = {}

    def record_name(self, character_id, name):
        character = self._find_or_create_character(character_id)
        character.name = name

    def record_birth(self, character_id, at, mom_id, sex):
        character = self._find_or_create_character(character_id)

        character.birth = at
        character.sex = sex

        self._record_relations(character, mom_id)

    def _find_or_create_character(self, character_id):
        if character_id not in self.characters:
            self.characters[character_id] = OholCharacter(character_id)
        return self.character(character_id)

    def _record_relations(self, character, mom_id):
        if mom_id is None:
            character.mark_as_eve()
            self.lineages[character.id] = Lineage(character)
        elif mom_id in self.characters:
            mom = self.character(mom_id)
            mom.add_kid(character)
        else:
            print('ERROR: unknown mom: ' + mom_id)

    def record_death(self, character_id, timestamp):
        character = self._find_or_create_character(character_id)
        character.death = timestamp

    def print_completeness_report(self):
        n_characters = len(self.characters)

        n_incomplete_characters = len(self.incomplete_characters())

        percent_incomplete = float(n_incomplete_characters) / n_characters * 100

        print("%s/%s = %.2f%% incomplete" % (n_incomplete_characters, n_characters, percent_incomplete))

    def incomplete_characters(self):
        return [c for c in self.characters.values() if not c.is_complete()]

    def complete_characters(self):
        return [c for c in self.characters.values() if c.is_complete()]

    def all_characters(self):
        return self.characters.values()

    def all_lineages(self):
        return self.lineages.values()

    def lineage(self, lineage_id):
        return self.lineages[lineage_id]

    def character(self, character_id):
        return self.characters[character_id]
