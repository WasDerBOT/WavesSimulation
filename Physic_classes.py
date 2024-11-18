from math import cos, sqrt, pi

from PyQt6.QtGui import QPainter, QColor

T = 1 / 30  # Period
k = 40


def k_abs(num):
    if num > 0:
        return num
    return 0


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
        temp = 255 - int((h + 1) * 255 / 2)
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
        self.normalize_fields()

    def process_heights(self):
        self.height += self.velocity


class Plane:
    def __init__(self, height, width):
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
                    self.points[i][j].mass = 5


    def shake(self, x, y):
        temp_cell_size = int(self.cellSize)
        x //= temp_cell_size
        y //= temp_cell_size
        size = self.brush_size // 2

        left_up, right_down = ((max(0, x - size // 2)), max(0, y - size // 2)), (
            min(self.width - 1, x + size // 2), min((self.height - 1), y + size // 2))
        for i in range(left_up[1], right_down[1]):
            for j in range(left_up[0], right_down[0]):
                tx = self.points[i][j].x - x
                ty = self.points[i][j].y - y
                r = sqrt(tx ** 2 + ty ** 2)
                if r <= (size / 2):
                    self.points[i][j].height = k_abs(
                        cos(tx * pi / (size / 2)) * cos(0 * ty * pi / (sqrt(size ** 2 - tx ** 2))) - abs(tx) / (
                                size / 2) - (ty / (size / 2)) ** 4)
                    self.points[i][j].normalize_fields()

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
