class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.characters = []

    def __str__(self):
        return f'{self.player_id} {len(self.characters)} lives'

    def add_character(self, character):
        self.characters.append(character)
