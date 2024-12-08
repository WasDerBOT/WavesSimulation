import math
from math import sqrt, pi

from PyQt6.QtGui import QPainter, QColor

T = 1 / 30  # Period
k = 20


def k_abs(num):
    if num > 0:
        return num
    return 0


def rotate_point(point1, point2, angle):
    x1, y1 = point1
    x2, y2 = point2

    dx = x1 - x2
    dy = y1 - y2

    nx = dx * math.cos(angle) - dy * math.sin(angle) + x2
    ny = dx * math.sin(angle) + dy * math.cos(angle) + y2

    return round(nx), round(ny)


class Point:
    def __init__(self, x, y, mass, height, velocity, plane, is_unmovable=False):
        self.x = x
        self.y = y
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.is_unmovable = is_unmovable
        self.plane = plane

    def draw(self, painter: QPainter):
        h = self.height
        if h > 0:
            temp = max(0, min(255 - int((h + 1) * 255 / 2), 254))
        else:
            temp = max(0, min(255 - int((h + 1) * 255 / 2), 254))
        tempCellSize = int(self.plane.cellSize)
        painter.fillRect(self.x * tempCellSize, self.y * tempCellSize, tempCellSize, tempCellSize,
                         QColor(temp, int(((temp / 255) ** (1 / self.mass)) * 255),
                                int(((temp / 255) ** (1 / self.mass ** 2)) * 255)))

    def __copy__(self):
        return Point(self.x, self.y, self.mass, self.height, self.velocity, self.plane, is_unmovable=self.is_unmovable)

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, height: {self.height} \n'

    def normalize_fields(self):
        self.height = max(-1, min(1, self.height))
        self.velocity = max(-1, min(1, self.velocity))

    def process_velocities(self, dx):
        if self.is_unmovable:
            return
        force = dx * k
        self.velocity += force * T / self.mass
        self.normalize_fields()

    def process_heights(self):
        self.height += self.velocity


class Plane:
    def __init__(self, height, width):
        self.env_mass = 1
        self.frame_count = 0
        self.height = height
        self.width = width
        self.cellSize = (550 / height)
        self.points = [[Point(i, k, 1, 0, 0, plane=self) for i in range(self.width)] for k in
                       range(self.height)]
        self.painter = None
        self.brush_size = 15
        self.initial_points = [[Point(i, k, 1, 0, 0, plane=self) for i in range(self.width)] for k in
                               range(self.height)]
        self.reset()

    def reset(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.points[i][j] = self.initial_points[i][j].__copy__()

    def draw(self, painter):
        if self.width == 1 and self.height == 1:
            return
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.points[i][j].draw(painter)

    def change_env(self, x, y):
        temp_cell_size = int(self.cellSize)
        x //= temp_cell_size
        y //= temp_cell_size
        size = self.brush_size
        left_up, right_down = ((max(0, x - size // 2)), max(0, y - size // 2)), (
            min(self.width - 1, x + size // 2), min((self.height - 1), y + size // 2))
        for i in range(left_up[1], right_down[1]):
            for j in range(left_up[0], right_down[0]):
                tx = self.points[i][j].x - x
                ty = self.points[i][j].y - y
                r = sqrt(tx ** 2 + ty ** 2)
                if r <= (size / 2):
                    self.points[i][j].mass = self.env_mass

    def shake(self, x, y, angle):
        temp_cell_size = int(self.cellSize)
        x //= temp_cell_size
        y //= temp_cell_size
        size = 10 + (3 * self.brush_size * abs(math.sin(self.frame_count * 0.3))) // 2

        for i in range(int(y - size // 2), int(y + size // 2)):
            for j in range(x, x + 1):
                tx = j - x
                ty = i - (y - size // 2)
                j, i = rotate_point((j, i), (x, y), -angle)
                j = min(max(j, 0), self.width - 1)
                i = min(max(i, 0), self.height - 1)
                if self.frame_count <= 30:
                    self.points[i][j].height = math.sin(self.frame_count * 0.3) * (math.sin(ty * pi / size) ** 4)


                j, i = rotate_point((j, i), (x, y), angle)

                for delta in range(2, 5):

                    j, i = rotate_point((j - delta, i), (x, y), -angle)
                    j = min(max(j, 0), self.width - 1)
                    i = min(max(i, 0), self.height - 1)
                    self.points[i][j].height = 0
                    self.points[i][j].velocity = 0
                    j, i = rotate_point((j - delta, i), (x, y), +angle)
        # self.points[int(y - size // 2) - 1][x].height = 0
        # self.points[int(y + size // 2) + 1][x].height = 0
        # self.points[int(y - size // 2) - 1][x].velocity = 0
        # self.points[int(y + size // 2) + 1][x].velocity = 0

    def process(self):
        if self.width < 5 and self.height < 5:
            return

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                dx = (self.points[i - 1][j].height + self.points[i + 1][j].height + self.points[i][j - 1].height + \
                      self.points[i][j + 1].height) / 4 - self.points[i][j].height
                self.points[i][j].process_velocities(dx)

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.points[i][j].process_heights()
