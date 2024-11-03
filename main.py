import sys

from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.uic import loadUi

from Physic_classes import Plane


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.painter = QPainter(self)


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
window = Main()
Field = Plane(550, 650, window.painter)
entry = Entry()
create = Create()

window.show()

sys.exit(app.exec())
