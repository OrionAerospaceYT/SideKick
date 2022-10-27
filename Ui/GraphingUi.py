# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphingUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(834, 536)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontal_divider = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.horizontal_divider.setObjectName("horizontal_divider")
        self.gridLayout.addWidget(self.horizontal_divider, 3, 8, 1, 2)
        self.top_bar = QtWidgets.QFrame(self.centralwidget)
        self.top_bar.setFrameShape(QtWidgets.QFrame.HLine)
        self.top_bar.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.top_bar.setObjectName("top_bar")
        self.gridLayout.addWidget(self.top_bar, 1, 0, 1, 11)
        self.terminal_divider = QtWidgets.QFrame(self.centralwidget)
        self.terminal_divider.setFrameShape(QtWidgets.QFrame.VLine)
        self.terminal_divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.terminal_divider.setObjectName("terminal_divider")
        self.gridLayout.addWidget(self.terminal_divider, 2, 7, 3, 1)
        self.bottom_widget = QtWidgets.QWidget(self.centralwidget)
        self.bottom_widget.setObjectName("bottom_widget")
        self.gridLayout.addWidget(self.bottom_widget, 4, 8, 1, 2)
        self.device = QtWidgets.QPushButton(self.centralwidget)
        self.device.setObjectName("device")
        self.gridLayout.addWidget(self.device, 0, 3, 1, 1)
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        self.terminal.setObjectName("terminal")
        self.gridLayout.addWidget(self.terminal, 2, 2, 3, 5)
        self.file = QtWidgets.QPushButton(self.centralwidget)
        self.file.setObjectName("file")
        self.gridLayout.addWidget(self.file, 0, 2, 1, 1)
        self.top_widget = QtWidgets.QWidget(self.centralwidget)
        self.top_widget.setObjectName("top_widget")
        self.gridLayout.addWidget(self.top_widget, 2, 8, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 8, 1, 1)
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 5, 2, 1, 4)
        self.help = QtWidgets.QPushButton(self.centralwidget)
        self.help.setObjectName("help")
        self.gridLayout.addWidget(self.help, 0, 9, 1, 1)
        self.record = QtWidgets.QPushButton(self.centralwidget)
        self.record.setObjectName("record")
        self.gridLayout.addWidget(self.record, 0, 5, 1, 2)
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setObjectName("send")
        self.gridLayout.addWidget(self.send, 5, 6, 1, 1)
        self.file_layout = QtWidgets.QFrame(self.centralwidget)
        self.file_layout.setEnabled(True)
        self.file_layout.setMinimumSize(QtCore.QSize(0, 0))
        self.file_layout.setStyleSheet("")
        self.file_layout.setObjectName("file_layout")
        self.file_menu = QtWidgets.QVBoxLayout(self.file_layout)
        self.file_menu.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.file_menu.setContentsMargins(20, -1, 20, -1)
        self.file_menu.setObjectName("file_menu")
        self.project_name = QtWidgets.QLineEdit(self.file_layout)
        self.project_name.setObjectName("project_name")
        self.file_menu.addWidget(self.project_name)
        self.select_project = QtWidgets.QComboBox(self.file_layout)
        self.select_project.setObjectName("select_project")
        self.select_project.addItem("")
        self.file_menu.addWidget(self.select_project)
        self.new_project = QtWidgets.QPushButton(self.file_layout)
        self.new_project.setObjectName("new_project")
        self.file_menu.addWidget(self.new_project)
        self.delete_project = QtWidgets.QPushButton(self.file_layout)
        self.delete_project.setObjectName("delete_project")
        self.file_menu.addWidget(self.delete_project)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.file_menu.addItem(spacerItem1)
        self.gridLayout.addWidget(self.file_layout, 2, 0, 4, 1)
        self.device_layout = QtWidgets.QFrame(self.centralwidget)
        self.device_layout.setObjectName("device_layout")
        self.dhsgd = QtWidgets.QVBoxLayout(self.device_layout)
        self.dhsgd.setContentsMargins(20, -1, 20, -1)
        self.dhsgd.setObjectName("dhsgd")
        self.com_ports = QtWidgets.QComboBox(self.device_layout)
        self.com_ports.setObjectName("com_ports")
        self.dhsgd.addWidget(self.com_ports)
        self.baud_rate = QtWidgets.QComboBox(self.device_layout)
        self.baud_rate.setObjectName("baud_rate")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.dhsgd.addWidget(self.baud_rate)
        self.supported_boards = QtWidgets.QComboBox(self.device_layout)
        self.supported_boards.setObjectName("supported_boards")
        self.dhsgd.addWidget(self.supported_boards)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dhsgd.addItem(spacerItem2)
        self.disconnect = QtWidgets.QPushButton(self.device_layout)
        self.disconnect.setObjectName("disconnect")
        self.dhsgd.addWidget(self.disconnect)
        self.library_manager = QtWidgets.QPushButton(self.device_layout)
        self.library_manager.setObjectName("library_manager")
        self.dhsgd.addWidget(self.library_manager)
        self.gridLayout.addWidget(self.device_layout, 2, 1, 4, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SideKick"))
        self.device.setText(_translate("MainWindow", "Device"))
        self.file.setText(_translate("MainWindow", "File"))
        self.pushButton.setText(_translate("MainWindow", "Upload"))
        self.help.setText(_translate("MainWindow", "Help"))
        self.record.setText(_translate("MainWindow", "Rec"))
        self.send.setText(_translate("MainWindow", "Send"))
        self.select_project.setItemText(0, _translate("MainWindow", "Select Project"))
        self.new_project.setText(_translate("MainWindow", "New Project"))
        self.delete_project.setText(_translate("MainWindow", "Delete Project"))
        self.baud_rate.setItemText(0, _translate("MainWindow", "115200"))
        self.baud_rate.setItemText(1, _translate("MainWindow", "57600"))
        self.baud_rate.setItemText(2, _translate("MainWindow", "38400"))
        self.baud_rate.setItemText(3, _translate("MainWindow", "9200"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.library_manager.setText(_translate("MainWindow", "Library Manager"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
