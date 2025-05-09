# Form implementation generated from reading ui file 'create.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Create(object):
    def setupUi(self, Create):
        Create.setObjectName("Create")
        Create.resize(800, 600)
        Create.setFixedSize(800, 600)
        self.tittle = QtWidgets.QLabel(parent=Create)
        self.tittle.setGeometry(QtCore.QRect(10, 10, 781, 111))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.tittle.setFont(font)
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tittle.setObjectName("tittle")
        self.horizontalSlider = QtWidgets.QSlider(parent=Create)
        self.horizontalSlider.setGeometry(QtCore.QRect(50, 440, 711, 61))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setRange(1, 10)
        self.ResolutionLbl = QtWidgets.QLabel(parent=Create)
        self.ResolutionLbl.setGeometry(QtCore.QRect(60, 160, 701, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ResolutionLbl.setFont(font)
        self.ResolutionLbl.setObjectName("label")
        self.TotalPointsLbl = QtWidgets.QLabel(parent=Create)
        self.TotalPointsLbl.setGeometry(QtCore.QRect(60, 300, 701, 91))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.TotalPointsLbl.setFont(font)
        self.TotalPointsLbl.setObjectName("label_2")
        self.CreateBtn = QtWidgets.QPushButton(parent=Create)
        self.CreateBtn.setGeometry(QtCore.QRect(150, 510, 291, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.CreateBtn.setFont(font)
        self.CreateBtn.setObjectName("Create_2")
        self.GoBackBtn = QtWidgets.QPushButton(parent=Create)
        self.GoBackBtn.setGeometry(QtCore.QRect(600, 510, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.GoBackBtn.setFont(font)
        self.GoBackBtn.setObjectName("Create_3")

        self.retranslateUi(Create)
        QtCore.QMetaObject.connectSlotsByName(Create)

    def retranslateUi(self, Create):
        _translate = QtCore.QCoreApplication.translate
        Create.setWindowTitle(_translate("Create", "Waves simulation"))
        self.tittle.setText(_translate("Create", "Field creation"))
        self.ResolutionLbl.setText(_translate("Create", "Resolution: {height} x {width}"))
        self.TotalPointsLbl.setText(_translate("Create", "Total points: {height * width}"))
        self.CreateBtn.setText(_translate("Create", "Create"))
        self.GoBackBtn.setText(_translate("Create", "Go back"))
        with open("templates/stylesheets/create.css", "r") as f:
            stylesheet = f.read()
        Create.setStyleSheet(stylesheet)
