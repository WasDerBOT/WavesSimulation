import sys

from PyQt6.QtCore import QTimer, QStringListModel
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QListView
from PyQt6.QtWidgets import QWidget, QMainWindow
from templates.main_window import Ui_MainWindow
from templates.entry import Ui_Greeting
from templates.create import Ui_Create
from templates.load import Ui_Load
from templates.save import Ui_Save
from templates.menu import Ui_Menu
from Physic_classes import Plane


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, plane: Plane):
        super().__init__()
        self.setupUi(self)
        plane.painter = QPainter(self)
        self.timer = QTimer()
        self.timer.timeout.connect(plane.process)
        # self.timer.start(30)
        self.painter = QPainter(self)


class Entry(QWidget, Ui_Greeting):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Create(QWidget, Ui_Create):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Load(QWidget, Ui_Load):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listView = self.findChild(QListView, "listView")
        self.model = QStringListModel()
        self.listView.setModel(self.model)
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), "First save example")
        self.model.insertRow(1)
        self.model.setData(self.model.index(1, 0), "Second save example")


class Save(QWidget, Ui_Save):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listView = self.findChild(QListView, "listView")
        self.model = QStringListModel()
        self.listView.setModel(self.model)
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), "First save example")
        self.model.insertRow(1)
        self.model.setData(self.model.index(1, 0), "Second save example")


class Menu(QWidget, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


FPS = 30
Frequency = 1 / FPS

app = QApplication(sys.argv)

Field = Plane(550, 650)
window = Main(Field)
entry = Entry()
create = Create()
load = Load()
save = Save()
load.show()
save.show()
create.show()
entry.show()
window.show()
menu = Menu()
menu.show()
sys.exit(app.exec())
