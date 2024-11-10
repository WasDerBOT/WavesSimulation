from math import cos, sqrt, pi

from PyQt6.QtGui import QPainter, QColor

T = 0.066  # Period
k = 10


class Point:
    def __init__(self, x, y, mass, height, velocity, is_unmovable=False):
        self.x = x
        self.y = y
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.is_unmovable = is_unmovable

    def draw(self, painter: QPainter):
        temp = 255 - int((self.height + 1) * 255 / 2)
        painter.fillRect(self.x * 10, self.y * 10, 10, 10, QColor(temp, temp, temp))

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, height: {self.height} \n'

    def normalize_height(self):
        self.height = max(-1, min(1, self.height))

    def process(self, dx):
        force = dx * k
        self.velocity += force * T / (self.mass)
        self.height = max(min(self.height + self.velocity, 1), -1)


class Plane:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.reset()
        self.painter = None

    def reset(self):
        self.points = [[Point(i, k, 1, 0.5, 0) for i in range(self.width)] for k in range(self.height)]

    def draw(self, painter):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.points[i][j].draw(painter)

    def shake(self, x, y):
        x //= 10
        y //= 10
        size = 15
        left_up, right_down = ((max(0, x - size // 2)), max(0, y - size // 2)), (
            min(self.width - 1, x + size // 2), min((self.height - 1), y + size // 2))
        for i in range(left_up[1], right_down[1]):
            for j in range(left_up[0], right_down[0]):

                tx = self.points[i][j].x - x
                ty = self.points[i][j].y - y
                r = sqrt(tx ** 2 + ty ** 2)
                if 0 < r <= (size / 2):
                    self.points[i][j].height += cos(r * pi / size)
                    self.points[i][j].normalize_height()

    def process(self):

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                dx = (self.points[i - 1][j].height + self.points[i + 1][j].height + self.points[i][j - 1].height + \
                      self.points[i][j + 1].height) / 4 - self.points[i][j].height
                self.points[i][j].process(dx)
