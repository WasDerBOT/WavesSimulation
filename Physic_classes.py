Frequency = 1 / 30


class Point:
    def __init__(self, mass, height, velocity, is_unmovable=False):
        self.mass = mass
        self.height = height
        self.velocity = velocity
        self.is_unmovable = is_unmovable

    def draw(self, painter):
        pass

    def process(self, point_up, point_down, point_left, point_right):
        force = point_up.height + point_down.height + point_left.height + point_right.height
        self.velocity += force / (Frequency * self.mass)


class Plane:
    def __init__(self, height, width, painter):
        self.height = height
        self.width = width
        self.points = [[Point(1, 0, 0) for i in range(width)] for k in range(height)]
        self.painter = painter

    def draw(self):
        for row in self.points:
            for point in row:
                point.draw(self.painter)

    def process(self):
        for i in range(self.height):
            for j in range(self.width):
                # Если точка находится на границе и с какой-то от нее стороны не существует точки, то мы передаем недвижимую точку.
                self.points[i][j].process(self.points[i - 1][j] if (i > 0) else Point(1, 0, 0, is_unmovable=True),
                                          self.points[i + 1][j] if (i < self.height - 1) else Point(1, 0, 0,
                                                                                                    is_unmovable=True),
                                          self.points[i][j - 1] if (i > 0) else Point(1, 0, 0, is_unmovable=True),
                                          self.points[i][j + 1] if (i < self.width - 1) else Point(1, 0, 0,
                                                                                                   is_unmovable=True), )
