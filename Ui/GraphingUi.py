# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphingUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 536)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("/*General Styling*/\n"
"* {\n"
"  \n"
"  font: 10pt \"Roboto \";\n"
"  font-size: 14px;\n"
"  background-color: #32323C;\n"
"  color: #FFFFFF;\n"
"}\n"
"\n"
"/*Button Styling*/\n"
"QPushButton {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #252535;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"}\n"
"QPushButton#upload {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  text-align: right;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#send {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#help {\n"
"  image: url(Ui/Help.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#new_project {\n"
"  image: url(Ui/Folder.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#disconnect {\n"
"  image: url(Ui/Plug.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#render {\n"
"  image: url(Ui/SideKick_White.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 20px;\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QPushButton:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Combo Box Styling*/\n"
"QComboBox {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #252535;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QComboBox:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"QComboBox:editable {\n"
"  background: #252535;\n"
"}\n"
"  QComboBox:!editable,\n"
"  QComboBox::drop-down:editable,\n"
"  QComboBox:!editable:on,\n"
"  QComboBox::drop-down:editable:on {\n"
"  background: #252535;\n"
"}\n"
"QComboBox::drop-down {\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: top right;\n"
"  border-left: none;\n"
"  color: #00f0c3;\n"
"}\n"
"QComboBox::down-arrow {\n"
"  image: url(Ui/D_Arrow.png);\n"
"  image-position: right;\n"
"  padding-right: 50px;\n"
"  width: 50px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"  background: #252535;\n"
"  border: none;\n"
"  color: #00f0c3;\n"
"}\n"
"\n"
"/*Line Edit Styling*/\n"
"QLineEdit {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 20px;\n"
"  height: 20px;\n"
"}\n"
"QLineEdit:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Label Styling*/\n"
"QLabel {\n"
"  font-size: 20px;\n"
"  font-weight: bold;\n"
"}\n"
"\n"
"/*Text Box Styling*/\n"
"QTextBrowser {\n"
"  border: none; \n"
"  padding-left:10px; \n"
"  padding-top:10px;\n"
"  background-color: #2b2b35;\n"
"  border-radius: 10px;\n"
"}\n"
"\n"
"QMenuBar {\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Removes the border from the scroll area*/\n"
"QScrollArea {\n"
"  border: none;\n"
"}\n"
"\n"
"/*Changes the graphs colours*/\n"
"QWidget #top_widget{\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  background-color: #2b2b35;\n"
"}\n"
"QWidget #bottom_widget{\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  background-color: #2b2b35;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 4, 1, 1)
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 5, 4, 1, 2)
        self.bottom_update = QtWidgets.QLabel(self.centralwidget)
        self.bottom_update.setText("")
        self.bottom_update.setObjectName("bottom_update")
        self.gridLayout.addWidget(self.bottom_update, 5, 6, 1, 2)
        self.bottom_widget = QtWidgets.QWidget(self.centralwidget)
        self.bottom_widget.setObjectName("bottom_widget")
        self.gridLayout.addWidget(self.bottom_widget, 3, 6, 1, 2)
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        self.horizontalFrame.setStyleSheet("/*General Styling*/\n"
"* {\n"
"  font: 12pt \"Roboto \";\n"
"  background-color: #25252f;\n"
"  color: #FFFFFF;\n"
"}\n"
"\n"
"/*Button Styling*/\n"
"QPushButton {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"}\n"
"QPushButton#upload {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  text-align: right;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#send {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#help {\n"
"  image: url(Ui/Help.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#new_project {\n"
"  image: url(Ui/Folder.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#disconnect {\n"
"  image: url(Ui/Plug.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#render {\n"
"  image: url(Ui/SideKick_White.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 20px;\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QPushButton:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Combo Box Styling*/\n"
"QComboBox {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #252535;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QComboBox:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"QComboBox:editable {\n"
"  background: #252535;\n"
"}\n"
"  QComboBox:!editable,\n"
"  QComboBox::drop-down:editable,\n"
"  QComboBox:!editable:on,\n"
"  QComboBox::drop-down:editable:on {\n"
"  background: #252535;\n"
"}\n"
"QComboBox::drop-down {\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: top right;\n"
"  border-left: none;\n"
"  color: #00f0c3;\n"
"}\n"
"QComboBox::down-arrow {\n"
"  image: url(Ui/D_Arrow.png);\n"
"  image-position: right;\n"
"  padding-right: 50px;\n"
"  width: 50px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"  background: #252535;\n"
"  border: none;\n"
"  color: #00f0c3;\n"
"}\n"
"\n"
"/*Line Edit Styling*/\n"
"QLineEdit {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #252535;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QLineEdit:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Label Styling*/\n"
"QLabel {\n"
"  font-size: 20px;\n"
"  font-weight: bold;\n"
"  padding-left: 6px;\n"
"}\n"
"\n"
"/*Text Box Styling*/\n"
"QTextBrowser {\n"
"  border: none;\n"
"  padding-left: 40px;\n"
"  background-color: #171727;\n"
"}\n"
"\n"
"QMenuBar {\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Removes the border from the scroll area*/\n"
"QScrollArea {\n"
"  border: none;\n"
"}")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file = QtWidgets.QPushButton(self.horizontalFrame)
        self.file.setObjectName("file")
        self.horizontalLayout.addWidget(self.file)
        self.device = QtWidgets.QPushButton(self.horizontalFrame)
        self.device.setObjectName("device")
        self.horizontalLayout.addWidget(self.device)
        self.upload = QtWidgets.QPushButton(self.horizontalFrame)
        self.upload.setObjectName("upload")
        self.horizontalLayout.addWidget(self.upload)
        self.record = QtWidgets.QPushButton(self.horizontalFrame)
        self.record.setObjectName("record")
        self.horizontalLayout.addWidget(self.record)
        self.record_light = QtWidgets.QLabel(self.horizontalFrame)
        self.record_light.setText("")
        self.record_light.setObjectName("record_light")
        self.horizontalLayout.addWidget(self.record_light)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.top_update = QtWidgets.QLabel(self.horizontalFrame)
        self.top_update.setText("")
        self.top_update.setObjectName("top_update")
        self.horizontalLayout.addWidget(self.top_update)
        self.help = QtWidgets.QPushButton(self.horizontalFrame)
        self.help.setObjectName("help")
        self.horizontalLayout.addWidget(self.help)
        self.gridLayout.addWidget(self.horizontalFrame, 0, 0, 1, 9)
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.top_widget = QtWidgets.QWidget(self.centralwidget)
        self.top_widget.setObjectName("top_widget")
        self.gridLayout.addWidget(self.top_widget, 1, 6, 2, 2)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 8, 1, 1)
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        self.terminal.setStyleSheet("")
        self.terminal.setObjectName("terminal")
        self.gridLayout.addWidget(self.terminal, 1, 4, 3, 2)
        self.file_layout = QtWidgets.QFrame(self.centralwidget)
        self.file_layout.setEnabled(True)
        self.file_layout.setMinimumSize(QtCore.QSize(200, 0))
        self.file_layout.setMaximumSize(QtCore.QSize(200, 16777215))
        self.file_layout.setStyleSheet("/*General Styling*/\n"
"* {\n"
"   font: 10pt \"Roboto \";\n"
"  background-color: #2b2b35;\n"
"  color: #FFFFFF;\n"
"  border: none;\n"
"  border-radius:10px;\n"
"}\n"
"\n"
"/*Button Styling*/\n"
"QPushButton {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"}\n"
"QPushButton#upload {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  text-align: right;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#send {\n"
"  image: url(Ui/U_Arrow.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#help {\n"
"  image: url(Ui/Help.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#new_project {\n"
"  image: url(Ui/Folder.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#disconnect {\n"
"  image: url(Ui/Plug.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton#render {\n"
"  image: url(Ui/SideKick_White.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 20px;\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QPushButton:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Combo Box Styling*/\n"
"QComboBox {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QComboBox:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"QComboBox:editable {\n"
"  background: #25252f;\n"
"}\n"
"  QComboBox:!editable,\n"
"  QComboBox::drop-down:editable,\n"
"  QComboBox:!editable:on,\n"
"  QComboBox::drop-down:editable:on {\n"
"  background: #25252f;\n"
"}\n"
"QComboBox::drop-down {\n"
"  subcontrol-origin: padding;\n"
"  subcontrol-position: top right;\n"
"  border-left: none;\n"
"  color: #00f0c3;\n"
"}\n"
"QComboBox::down-arrow {\n"
"  image: url(Ui/D_Arrow.png);\n"
"  image-position: right;\n"
"  padding-right: 50px;\n"
"  width: 50px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"  background: #252535;\n"
"  border: none;\n"
"  color: #00f0c3;\n"
"}\n"
"\n"
"/*Line Edit Styling*/\n"
"QLineEdit {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QLineEdit:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Label Styling*/\n"
"QLabel {\n"
"  font-size: 20px;\n"
"  font-weight: bold;\n"
"  padding-left: 6px;\n"
"}\n"
"\n"
"/*Text Box Styling*/\n"
"QTextBrowser {\n"
"  border: none;\n"
"  padding-left: 40px;\n"
"  /*border-image: url(Ui/Schematic.png) 0 0 0 0 strech strech;*/\n"
"}\n"
"\n"
"QMenuBar {\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Removes the border from the scroll area*/\n"
"QScrollArea {\n"
"  border: none;\n"
"}")
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
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.file_menu.addItem(spacerItem4)
        self.gridLayout.addWidget(self.file_layout, 1, 1, 5, 1)
        self.device_layout = QtWidgets.QFrame(self.centralwidget)
        self.device_layout.setMinimumSize(QtCore.QSize(200, 0))
        self.device_layout.setMaximumSize(QtCore.QSize(200, 16777215))
        self.device_layout.setStyleSheet("/*General Styling*/\n"
"* {\n"
"   font: 10pt \"Roboto \";\n"
"  font-size: 14px;\n"
"  background-color: #2b2b35;\n"
"  color: #FFFFFF;\n"
"  border:none;\n"
"  border-radius:10px;\n"
"}\n"
"\n"
"/*Button Styling*/\n"
"QPushButton {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"}\n"
"QPushButton#disconnect {\n"
"  image: url(Ui/Plug.png);\n"
"  image-position: left;\n"
"  padding-left: 10px;\n"
"  width: 10px;\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QPushButton:hover:!pressed{\n"
"  background-color: #151525;\n"
"}\n"
"\n"
"/*Combo Box Styling*/\n"
"QComboBox {\n"
"  padding: 10px 10px;\n"
"  text-align: center;\n"
"  outline: none;\n"
"  background-color: #25252f;\n"
"  border: none;\n"
"  border-radius: 10px;\n"
"  height: 20px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"  image: url(Ui/D_Arrow.png);\n"
"  image-position: right;\n"
"  padding-right: 50px;\n"
"  width: 50px;\n"
"  height: 20px;\n"
"}\n"
"\n"
"/*Label Styling*/\n"
"QLabel {\n"
"  font-size: 20px;\n"
"  font-weight: bold;\n"
"  padding-left: 6px;\n"
"}")
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
        self.disconnect = QtWidgets.QPushButton(self.device_layout)
        self.disconnect.setObjectName("disconnect")
        self.dhsgd.addWidget(self.disconnect)
        self.library_manager = QtWidgets.QPushButton(self.device_layout)
        self.library_manager.setObjectName("library_manager")
        self.dhsgd.addWidget(self.library_manager)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dhsgd.addItem(spacerItem5)
        self.gridLayout.addWidget(self.device_layout, 1, 2, 5, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_3.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 4, 4, 1, 4)
        self.gridLayout.setColumnStretch(4, 3)
        self.gridLayout.setColumnStretch(6, 5)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SideKick"))
        self.file.setText(_translate("MainWindow", "File"))
        self.device.setText(_translate("MainWindow", "Device"))
        self.upload.setText(_translate("MainWindow", "Upload"))
        self.record.setText(_translate("MainWindow", "Record"))
        self.help.setText(_translate("MainWindow", "Help"))
        self.select_project.setItemText(0, _translate("MainWindow", "Select Project"))
        self.new_project.setText(_translate("MainWindow", "New Project"))
        self.delete_project.setText(_translate("MainWindow", "Delete Project"))
        self.baud_rate.setItemText(0, _translate("MainWindow", "115200"))
        self.baud_rate.setItemText(1, _translate("MainWindow", "57600"))
        self.baud_rate.setItemText(2, _translate("MainWindow", "38400"))
        self.baud_rate.setItemText(3, _translate("MainWindow", "9200"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.library_manager.setText(_translate("MainWindow", "Library Manager"))
        self.pushButton_3.setText(_translate("MainWindow", "x"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
