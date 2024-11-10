from PyQt6.QtGui import QPainter, QPen, QColor, QBrush

T = 1 / 66  # Period


class Point:
    def __init__(self, x, y, mass, height, velocity, is_unmovable=False):
        self.x = x
        self.y = y
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.is_unmovable = is_unmovable

    def draw(self, painter: QPainter):
        temp = int((self.height + 1) * 255 / 2)
        color = QColor.fromRgba64(temp, temp, temp, 255)
        painter.setBrush(color)
        painter.drawRect(self.x * 10, self.y * 10, 10, 10)

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, height: {self.height} \n'

    def process(self, force):
        self.velocity += force / (T * self.mass * 10)
        self.height = max(min(self.height + self.velocity, 1), -1)


class Plane:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.points = [[Point(i, k, 1, 0.5, 0) for i in range(width)] for k in range(height)]
        self.painter = None

    def draw(self, painter):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.points[i][j].draw(painter)

    def process(self):

        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                force = self.points[i - 1][j].height + self.points[i + 1][j].height + self.points[i][j - 1].height + \
                        self.points[i][j + 1].height
                self.points[i][j].process(force)
