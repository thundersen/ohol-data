class Lineage:
    def __init__(self, eve):
        self.eve = eve

    def characters(self):
        return [self.eve] + self.eve.descendants()
