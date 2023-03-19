# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ActuatorUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(513, 376)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.actuator = QtWidgets.QLabel(self.centralwidget)
        self.actuator.setObjectName("actuator")
        self.verticalLayout.addWidget(self.actuator)
        self.pin = QtWidgets.QLabel(self.centralwidget)
        self.pin.setObjectName("pin")
        self.verticalLayout.addWidget(self.pin)
        self.pos = QtWidgets.QLabel(self.centralwidget)
        self.pos.setObjectName("pos")
        self.verticalLayout.addWidget(self.pos)
        self.gridLayout.addLayout(self.verticalLayout, 6, 0, 1, 2)
        self.new_actuator = QtWidgets.QVBoxLayout()
        self.new_actuator.setObjectName("new_actuator")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setObjectName("name")
        self.new_actuator.addWidget(self.name)
        self.pin_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pin_input.setObjectName("pin_input")
        self.new_actuator.addWidget(self.pin_input)
        self.select_actuator = QtWidgets.QComboBox(self.centralwidget)
        self.select_actuator.setObjectName("select_actuator")
        self.new_actuator.addWidget(self.select_actuator)
        self.add_actuator = QtWidgets.QPushButton(self.centralwidget)
        self.add_actuator.setObjectName("add_actuator")
        self.new_actuator.addWidget(self.add_actuator)
        self.gridLayout.addLayout(self.new_actuator, 6, 2, 1, 1)
        self.upper_lim = QtWidgets.QLineEdit(self.centralwidget)
        self.upper_lim.setObjectName("upper_lim")
        self.gridLayout.addWidget(self.upper_lim, 4, 2, 1, 1)
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.gridLayout.addWidget(self.slider, 2, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 5, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 3, 1, 1, 1)
        self.lower_lim = QtWidgets.QLineEdit(self.centralwidget)
        self.lower_lim.setObjectName("lower_lim")
        self.gridLayout.addWidget(self.lower_lim, 4, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scroll = QtWidgets.QWidget()
        self.scroll.setGeometry(QtCore.QRect(0, 0, 474, 113))
        self.scroll.setObjectName("scroll")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.scroll)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 20, 160, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.slider_area = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.slider_area.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.slider_area.setContentsMargins(0, 0, 0, 0)
        self.slider_area.setObjectName("slider_area")
        self.horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.slider_area.addWidget(self.horizontalSlider)
        self.scrollArea.setWidget(self.scroll)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Actuator Tuning"))
        self.actuator.setText(_translate("MainWindow", "Actuator: "))
        self.pin.setText(_translate("MainWindow", "Pin: "))
        self.pos.setText(_translate("MainWindow", "Position"))
        self.add_actuator.setText(_translate("MainWindow", "Add Actuator"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
