import sys

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt6.uic import loadUi


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
