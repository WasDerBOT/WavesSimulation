import sys

from PyQt6.QtCore import QTimer, QStringListModel, QEvent
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QListView
from PyQt6.QtWidgets import QWidget, QMainWindow

from Physic_classes import Plane
from templates.create import Ui_Create
from templates.entry import Ui_Greeting
from templates.load import Ui_Load
from templates.main_window import Ui_MainWindow
from templates.menu import Ui_Menu
from templates.save import Ui_Save

tHeight, tWidth = 55, 65


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMouseTracking(True)
        self.plane = Plane(55, 65)
        self.timer = QTimer()
        self.timer.timeout.connect(self.process)
        self.SaveBtn.clicked.connect(self.to_save)
        self.ResetBtn.clicked.connect(self.reset)
        self.IsGoing = True
        self.Play_PauseBtn.clicked.connect(self.pause)

    def init_plane(self, plane: Plane):

        self.plane = plane
        print("2")

    def mousePressEvent(self, e: QEvent):
        x, y = e.pos().x(), e.pos().y()

        self.plane.shake(x, y)
        self.update()

    def reset(self):
        self.plane.reset()
        self.update()

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
        self.IsGoing = False
        self.Play_PauseBtn.clicked.connect(self.resume)
        self.Play_PauseBtn.setText("Play")

    def resume(self):
        self.timer.start(30)
        self.IsGoing = False
        self.Play_PauseBtn.clicked.connect(self.pause)
        self.Play_PauseBtn.setText("Play")

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
        value = self.horizontalSlider.value()
        height = int(tHeight * value * 0.2)
        width = int(tWidth * value * 0.2)
        window.plane = Plane(height, width)
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
        window.timer.start(30)


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
T = 1000 / FPS
Frequency = 1 / FPS

app = QApplication(sys.argv)

Field = Plane(110, 130)
save = Save()
window = Main()
load = Load()
create = Create()
menu = Menu()
entry = Entry()

entry.show()

sys.exit(app.exec())
