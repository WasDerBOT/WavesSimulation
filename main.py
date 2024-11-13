import sys

from PyQt6.QtCore import QTimer, QStringListModel, QEvent, Qt
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
FPS = 30
T = 1000 // FPS


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
        self.horizontalSlider.valueChanged.connect(self.set_brush_size)

    def set_brush_size(self):
        self.plane.brush_size = self.horizontalSlider.value()

    def init_plane(self, plane: Plane):
        self.plane = plane

    def mousePressEvent(self, event: QEvent):
        x, y = event.pos().x(), event.pos().y()
        if event.button() == Qt.MouseButton.LeftButton:
            self.plane.shake(x, y)
        elif event.button() == Qt.MouseButton.RightButton:
            self.plane.change_env(x, y)
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
        self.timer.start(T)
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
        window.timer.start(T)

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
