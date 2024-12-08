import os
import sqlite3
import sys
from math import acos, pi

from PyQt6.QtCore import QTimer, QStringListModel, QEvent, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QListView
from PyQt6.QtWidgets import QWidget, QMainWindow

from Physic_classes import Plane
from config import *
from templates.create import Ui_Create
from templates.entry import Ui_Greeting
from templates.load import Ui_Load
from templates.main_window import Ui_MainWindow
from templates.menu import Ui_Menu
from templates.save import Ui_Save

tHeight, tWidth = 55, 65


def angle_between(v1, v2):
    v1_norm = (v1[0] ** 2 + v1[1] ** 2) ** 0.5
    v2_norm = (v2[0] ** 2 + v2[1] ** 2) ** 0.5
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    angle = acos(dot_product / (v1_norm * v2_norm))
    return angle


conn = sqlite3.connect('fields.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS fields (id INTEGER PRIMARY KEY, name TEXT, file_name TEXT)''')


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.is_shaking = False
        self.shaking_angle = 0
        self.shaking_duration = 60
        self.shaking_position = (0, 0)
        self.setupUi(self)
        self.setMouseTracking(True)
        # Создаем заглушку плоскости
        self.plane = Plane(55, 65)
        # Создаем таймер для опработки физики
        self.timer = QTimer()
        self.timer.timeout.connect(self.process)
        self.SaveBtn.clicked.connect(self.to_save)
        self.ResetBtn.clicked.connect(self.reset)
        self.MenuBtn.clicked.connect(self.to_menu)
        self.IsGoing = True
        self.Play_PauseBtn.clicked.connect(self.pause)
        self.BrushSizeHorizontalSlider.valueChanged.connect(self.set_brush_size)

    def set_brush_size(self):
        self.plane.brush_size = self.BrushSizeHorizontalSlider.value()

    def init_plane(self, plane: Plane):
        self.plane = plane

    def mousePressEvent(self, event: QEvent):
        x, y = event.pos().x(), event.pos().y()
        self.shaking_position = (x, y)

    def mouseReleaseEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        x0, y0 = self.shaking_position
        if event.button() == Qt.MouseButton.LeftButton and not self.is_shaking and x in range(0,
                                                                                              int(self.plane.width * self.plane.cellSize) + 1) and y in range(
            0, int(self.plane.height * self.plane.cellSize) + 1):
            self.is_shaking = True
            self.plane.frame_count = 0
            self.shaking_angle = angle_between((x - x0, y - y0), (1, 0))
            print(self.shaking_angle / (2 * pi) * 360)
            if y - y0 > 0:
                self.shaking_angle = 2 * pi - self.shaking_angle
            print(x - x0, y - y0)
        elif event.button() == Qt.MouseButton.RightButton and not self.is_shaking and x in range(0,
                                                                                                 int(self.plane.width * self.plane.cellSize) + 1) and y in range(
            0, int(self.plane.height * self.plane.cellSize) + 1):
            self.plane.change_env(x0, y0)
        self.update()

    def reset(self):
        self.plane.reset()
        self.update()

    def process(self):
        if self.is_shaking:
            x, y = self.shaking_position
            self.plane.shake(x, y, self.shaking_angle)
        self.plane.process()
        self.plane.frame_count += 1
        if self.plane.frame_count >= self.shaking_duration:
            self.is_shaking = False
            self.plane.frame_count = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.plane.draw(painter)
        painter.end()

    def pause(self):
        self.timer.stop()
        self.IsGoing = False
        self.Play_PauseBtn.clicked.connect(self.resume)
        self.Play_PauseBtn.setText("Play")

    def resume(self):
        self.timer.start(T)
        self.IsGoing = False
        self.Play_PauseBtn.clicked.connect(self.pause)
        self.Play_PauseBtn.setText("Pause")

    def to_save(self):
        self.pause()
        self.hide()
        save.show()

    def to_menu(self):
        self.pause()
        self.hide()
        menu.show()


class Entry(QWidget, Ui_Greeting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.enterBtn.clicked.connect(self.enter)

    def enter(self):
        self.close()
        menu.show()


class Create(QWidget, Ui_Create):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.GoBackBtn.clicked.connect(self.go_back)
        self.CreateBtn.clicked.connect(self.create)
        self.horizontalSlider.valueChanged.connect(self.update_labels)
        height = int(tHeight * 1 * 0.2)
        width = int(tWidth * 1 * 0.2)
        self.ResolutionLbl.setText(f"Resolution: {width} x {height} points")
        self.TotalPointsLbl.setText(f"Total points: {height * width}")

    def update_labels(self):
        value = self.horizontalSlider.value()
        height = int(tHeight * value * 0.2)
        width = int(tWidth * value * 0.2)
        self.ResolutionLbl.setText(f"Resolution: {width} x {height} points")
        self.TotalPointsLbl.setText(f"Total points: {height * width}")

    def create(self):
        value = self.horizontalSlider.value()
        height = int(tHeight * value * 0.2)
        width = int(tWidth * value * 0.2)
        window.plane = Plane(height, width)
        self.hide()
        window.show()
        window.resume()

    def go_back(self):
        self.hide()
        menu.show()


class Load(QWidget, Ui_Load):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listView = self.findChild(QListView, "listView")
        self.model = QStringListModel()
        self.listView.setModel(self.model)
        self.GoBackBtn.clicked.connect(self.go_back)
        self.LoadBtn.clicked.connect(self.load)
        self.list_update()

    def go_back(self):
        self.hide()
        menu.show()

    def load(self):
        name = self.model.itemData(self.listView.currentIndex())
        file_name = c.execute(f"SELECT file_name FROM fields WHERE name = '{name[0]}'").fetchall()[0][0]
        with open(f"saves/{file_name}") as f:
            masses = f.readlines()
        height = int(masses[0])
        width = int(masses[1])
        masses.pop(0)
        masses.pop(0)
        window.plane = Plane(height, width)

        for i in range(0, height):
            for j in range(0, width):
                window.plane.points[i][j].mass = int(masses[i * width + j])
                window.plane.initial_points[i][j].mass = int(masses[i * width + j])

        self.hide()
        window.show()
        window.resume()

    def list_update(self):

        while self.model.rowCount():
            self.model.removeRow(0)
        data = c.execute("SELECT * FROM fields").fetchall()
        for line in data:
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount() - 1, 0), line[1])


class Save(QWidget, Ui_Save):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listView = self.findChild(QListView, "listView")
        self.model = QStringListModel()
        self.listView.setModel(self.model)
        self.GoBackBtn.clicked.connect(self.go_back)
        self.SaveBtn.clicked.connect(self.save)
        self.list_update()

    def go_back(self):
        self.hide()
        window.show()
        window.resume()

    def save(self):
        name = self.lineEdit.text()
        with open(f"saves/{name}.txt", mode="w") as f:
            f.write(str(window.plane.height) + "\n" + str(window.plane.width) + "\n")
            for i in range(0, window.plane.height):
                for j in range(0, window.plane.width):
                    f.write(str(window.plane.points[i][j].mass) + "\n")

        c.execute(f"INSERT INTO fields(name, file_name)  VALUES('{name}', '{name}.txt')")
        conn.commit()
        self.list_update()
        self.lineEdit.clear()

    def list_update(self):

        while self.model.rowCount():
            self.model.removeRow(0)
        data = c.execute("SELECT * FROM fields").fetchall()
        for line in data:
            self.model.insertRow(self.model.rowCount())
            self.model.setData(self.model.index(self.model.rowCount() - 1, 0), line[1])


class Menu(QWidget, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CreateBtn.clicked.connect(self.to_create)
        self.LoadBtn.clicked.connect(self.to_load)

    def to_load(self):
        self.hide()
        load.show()
        load.list_update()

    def to_create(self):
        self.hide()
        create.show()


# Создание папки для сохранений
try:
    os.mkdir("saves")
except FileExistsError:
    pass

app = QApplication(sys.argv)

# Создаем окна
save = Save()
window = Main()
load = Load()
create = Create()
menu = Menu()
entry = Entry()

entry.show()

sys.exit(app.exec())
