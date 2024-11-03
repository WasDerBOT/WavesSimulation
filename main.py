import sys

from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt6.uic import loadUi

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)


class Entry(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("entry.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    entry = Entry()
    sys.exit(app.exec())
