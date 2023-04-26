# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\LibraryUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(462, 404)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.search = QtWidgets.QLineEdit(self.centralwidget)
        self.search.setObjectName("search")
        self.gridLayout.addWidget(self.search, 1, 0, 1, 1)
        self.enter = QtWidgets.QPushButton(self.centralwidget)
        self.enter.setObjectName("enter")
        self.gridLayout.addWidget(self.enter, 1, 1, 1, 1)
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.gridLayout.addWidget(self.logo, 0, 0, 1, 2)
        self.install = QtWidgets.QPushButton(self.centralwidget)
        self.install.setObjectName("install")
        self.gridLayout.addWidget(self.install, 3, 0, 1, 2)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 423, 285))
        self.scrollAreaWidget.setObjectName("scrollAreaWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.libraries = QtWidgets.QVBoxLayout()
        self.libraries.setObjectName("libraries")
        self.verticalLayout_2.addLayout(self.libraries)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SideKick Library Manager"))
        self.enter.setText(_translate("MainWindow", "Enter"))
        self.install.setText(_translate("MainWindow", "Install"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
