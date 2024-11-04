import sys

from PyQt6.QtCore import QThread
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.uic import loadUi

from Physic_classes import Plane


class Main(QMainWindow):
    def __init__(self, plane: Plane):
        super().__init__()
        loadUi("main.ui", self)
        self.painter = QPainter(self)
        plane.painter = self.painter
        self.timer = QTimer()
        self.timer.timeout.connect(plane.process)
        self.timer.start(30)

    def update_screen(self):
        pass


class Entry(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("entry.ui", self)


class Create(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("create.ui", self)


FPS = 30
Frequency = 1 / FPS

app = QApplication(sys.argv)

Field = Plane(550, 650)
window = Main(Field)
entry = Entry()
create = Create()

window.show()

sys.exit(app.exec())
