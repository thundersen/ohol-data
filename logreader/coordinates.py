import math


class Coordinates:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def distance_from(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy)

    def distance_from_zero(self):
        return self.distance_from(Coordinates(0, 0))
