Frequency = 30

from PyQt6.QtGui import QPainter


class Point:
    def __init__(self, mass, height, velocity, is_unmovable=False):
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.is_unmovable = is_unmovable

    def draw(self, painter: QPainter):
        pass

    def process(self, painter, point_up, point_down, point_left, point_right):
        force = point_up.height + point_down.height + point_left.height + point_right.height
        self.velocity += force / (Frequency * self.mass)
        if self.velocity:
            self.draw(painter)
        self.height += self.velocity


class Plane:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.points = [[Point(1, 0, 0) for i in range(width)] for k in range(height)]
        self.painter = None

    def process(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                point_up = self.points[i - 1][j]
                point_down = self.points[i + 1][j]
                point_left = self.points[i][j - 1]
                point_right = self.points[i][j + 1]
                self.points[i][j].process(self.painter, point_up, point_down, point_left, point_right)
