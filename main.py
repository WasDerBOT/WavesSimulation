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
        self.plane = plane
        self.timer = QTimer()
        self.timer.timeout.connect(self.process)
        self.SaveBtn.clicked.connect(self.to_save)

    def process(self):
        self.plane.process()
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.plane.draw(painter)
        painter.end()


    def pause(self):
        self.timer.stop()

    def resume(self):
        self.timer.start(66)

    def to_save(self):
        self.pause()
        self.hide()
        save.show()


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

    def create(self):
        self.hide()
        window.show()
        window.timer.start(66)

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
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, 0), "First save example")
        self.model.insertRow(1)
        self.model.setData(self.model.index(1, 0), "Second save example")
        self.GoBackBtn.clicked.connect(self.go_back)

    def go_back(self):
        self.hide()
        menu.show()


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
        self.GoBackBtn.clicked.connect(self.go_back)

    def go_back(self):
        self.hide()
        window.show()
        window.timer.start(70)


class Menu(QWidget, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CreateBtn.clicked.connect(self.to_create)
        self.LoadBtn.clicked.connect(self.to_load)

    def to_load(self):
        self.hide()
        load.show()

    def to_create(self):
        self.hide()
        create.show()


FPS = 30
Frequency = 1 / FPS

app = QApplication(sys.argv)

Field = Plane(55, 65)
save = Save()
window = Main(Field)
load = Load()
create = Create()
menu = Menu()
entry = Entry()

entry.show()

sys.exit(app.exec())
