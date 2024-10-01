# Form implementation generated from reading ui file '.\ManagerUi.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 362)
        MainWindow.setMinimumSize(QtCore.QSize(485, 300))
        MainWindow.setStyleSheet("QScrollBar:vertical\n"
"{\n"
"    width: 8px;\n"
"    background: #32323C;\n"
"}\n"
"QScrollBar::add-page, QScrollBar::sub-page \n"
"{\n"
"    background-color: #32323C;\n"
"}\n"
"QScrollBar::add-line, QScrollBar::sub-line \n"
"{\n"
"    background-color: #32323C;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 639, 263))
        self.scrollAreaWidget.setObjectName("scrollAreaWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.selectable_items = QtWidgets.QVBoxLayout()
        self.selectable_items.setObjectName("selectable_items")
        self.verticalLayout_2.addLayout(self.selectable_items)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.install = QtWidgets.QPushButton(parent=self.centralwidget)
        self.install.setObjectName("install")
        self.horizontalLayout_2.addWidget(self.install)
        self.versions = QtWidgets.QComboBox(parent=self.centralwidget)
        self.versions.setObjectName("versions")
        self.versions.addItem("")
        self.horizontalLayout_2.addWidget(self.versions)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 3)
        self.search_bar = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.search_bar.setObjectName("search_bar")
        self.gridLayout.addWidget(self.search_bar, 0, 0, 1, 3)
        self.gridLayout_7.addLayout(self.gridLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Manager"))
        self.install.setText(_translate("MainWindow", "Install"))
        self.versions.setItemText(0, _translate("MainWindow", "N/A"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())