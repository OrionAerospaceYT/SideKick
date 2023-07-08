# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\GraphingUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1012, 694)
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
"QPushButton#send {\n"
"  image: url(Ui/U_Arrow.png);\n"
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
"QPushButton#quit{\n"
"  background-color: #2b2b35;\n"
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
"  background-color: #21212a;\n"
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
"}\n"
"\n"
"/*ScrollBar*/\n"
"QScrollBar\n"
"{\n"
"    width: 20px;\n"
"    border:none;\n"
"    border-radius: 10px;\n"
"    background: #2b2b35;\n"
"}\n"
"QScrollBar::add-page, QScrollBar::sub-page \n"
"{\n"
"    background-color: #2b2b35;\n"
"}\n"
"QScrollBar::add-line, QScrollBar::sub-line \n"
"{\n"
"    background-color: #2b2b35;\n"
"}\n"
"QScrollBar::handle\n"
"{\n"
"    background-color: grey;\n"
"    min-height: 30px;\n"
"    border-radius: 10px;\n"
"    border:none;\n"
"}\n"
"QScrollBar::up-arrow\n"
"{\n"
"    background: none;\n"
"}\n"
"QScrollBar::down-arrow\n"
"{\n"
"    background: none;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 3, 1, 1)
        self.bottom_update = QtWidgets.QLabel(self.centralwidget)
        self.bottom_update.setText("")
        self.bottom_update.setObjectName("bottom_update")
        self.gridLayout.addWidget(self.bottom_update, 5, 5, 1, 2)
        self.message = QtWidgets.QLineEdit(self.centralwidget)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 5, 3, 1, 2)
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
"QComboBox:hover:!pressed{\n"
"  background-color: #151525;\n"
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
        self.file.setMinimumSize(QtCore.QSize(0, 0))
        self.file.setObjectName("file")
        self.horizontalLayout.addWidget(self.file)
        self.device = QtWidgets.QPushButton(self.horizontalFrame)
        self.device.setMinimumSize(QtCore.QSize(0, 0))
        self.device.setObjectName("device")
        self.horizontalLayout.addWidget(self.device)
        self.upload = QtWidgets.QPushButton(self.horizontalFrame)
        self.upload.setMinimumSize(QtCore.QSize(0, 0))
        self.upload.setObjectName("upload")
        self.horizontalLayout.addWidget(self.upload)
        self.compile = QtWidgets.QPushButton(self.horizontalFrame)
        self.compile.setMinimumSize(QtCore.QSize(0, 0))
        self.compile.setObjectName("compile")
        self.horizontalLayout.addWidget(self.compile)
        self.com_ports = QtWidgets.QComboBox(self.horizontalFrame)
        self.com_ports.setMinimumSize(QtCore.QSize(0, 0))
        self.com_ports.setObjectName("com_ports")
        self.horizontalLayout.addWidget(self.com_ports)
        self.record = QtWidgets.QPushButton(self.horizontalFrame)
        self.record.setMinimumSize(QtCore.QSize(75, 0))
        self.record.setObjectName("record")
        self.horizontalLayout.addWidget(self.record)
        self.record_light = QtWidgets.QLabel(self.horizontalFrame)
        self.record_light.setText("")
        self.record_light.setObjectName("record_light")
        self.horizontalLayout.addWidget(self.record_light)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.top_update = QtWidgets.QLabel(self.horizontalFrame)
        self.top_update.setMinimumSize(QtCore.QSize(400, 0))
        self.top_update.setMaximumSize(QtCore.QSize(400, 16777215))
        self.top_update.setText("")
        self.top_update.setAlignment(QtCore.Qt.AlignCenter)
        self.top_update.setObjectName("top_update")
        self.horizontalLayout.addWidget(self.top_update)
        self.help = QtWidgets.QPushButton(self.horizontalFrame)
        self.help.setMinimumSize(QtCore.QSize(0, 0))
        self.help.setObjectName("help")
        self.horizontalLayout.addWidget(self.help)
        self.gridLayout.addWidget(self.horizontalFrame, 0, 0, 1, 8)
        self.bottom_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_widget.sizePolicy().hasHeightForWidth())
        self.bottom_widget.setSizePolicy(sizePolicy)
        self.bottom_widget.setMinimumSize(QtCore.QSize(0, 100))
        self.bottom_widget.setObjectName("bottom_widget")
        self.gridLayout.addWidget(self.bottom_widget, 3, 5, 1, 2)
        self.debugger = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.debugger.sizePolicy().hasHeightForWidth())
        self.debugger.setSizePolicy(sizePolicy)
        self.debugger.setStyleSheet("QFrame{\n"
"   font: 10pt \"Roboto \";\n"
"  font-size: 14px;\n"
"  background-color: #2b2b35;\n"
"  color: #FFFFFF;\n"
"  border:none;\n"
"  border-radius:10px;\n"
"}\n"
"")
        self.debugger.setObjectName("debugger")
        self.debugger_1 = QtWidgets.QGridLayout(self.debugger)
        self.debugger_1.setObjectName("debugger_1")
        self.quit = QtWidgets.QPushButton(self.debugger)
        self.quit.setStyleSheet("QPushButton:hover:!pressed{\n"
"  background-color: #ff0000;\n"
"}")
        self.quit.setObjectName("quit")
        self.debugger_1.addWidget(self.quit, 0, 2, 1, 1)
        self.full_screen = QtWidgets.QPushButton(self.debugger)
        self.full_screen.setStyleSheet("QPushButton{\n"
"   font: 10pt \"Roboto \";\n"
"  font-size: 14px;\n"
"  background-color: #2b2b35;\n"
"  color: #FFFFFF;\n"
"  border:none;\n"
"  border-radius:10px;\n"
"}\n"
"QPushButton:pressed {\n"
"  background-color: #000;\n"
"}\n"
"QPushButton:hover:!pressed{\n"
"  background-color: #151525;\n"
"}")
        self.full_screen.setObjectName("full_screen")
        self.debugger_1.addWidget(self.full_screen, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.debugger_1.addItem(spacerItem2, 0, 0, 1, 1)
        self.debug_log = QtWidgets.QTextBrowser(self.debugger)
        self.debug_log.setMinimumSize(QtCore.QSize(0, 150))
        self.debug_log.setStyleSheet("")
        self.debug_log.setObjectName("debug_log")
        self.debugger_1.addWidget(self.debug_log, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.debugger, 4, 3, 1, 4)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 6, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 6, 7, 1, 1)
        self.terminal = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.terminal.sizePolicy().hasHeightForWidth())
        self.terminal.setSizePolicy(sizePolicy)
        self.terminal.setStyleSheet("QScrollBar\n"
"{\n"
"    width: 20px;\n"
"    border:none;\n"
"    border-radius: 10px;\n"
"    background: #2b2b35;\n"
"}\n"
"QScrollBar::add-page, QScrollBar::sub-page \n"
"{\n"
"    background-color: #2b2b35;\n"
"}\n"
"QScrollBar::add-line, QScrollBar::sub-line \n"
"{\n"
"    background-color: #2b2b35;\n"
"}")
        self.terminal.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.terminal.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.terminal.setObjectName("terminal")
        self.gridLayout.addWidget(self.terminal, 1, 3, 3, 2)
        self.side_menu = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_menu.sizePolicy().hasHeightForWidth())
        self.side_menu.setSizePolicy(sizePolicy)
        self.side_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.side_menu.setMaximumSize(QtCore.QSize(200, 16777215))
        self.side_menu.setStyleSheet("/*General Styling*/\n"
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
"  font-size: 15px;\n"
"  font-weight: bold;\n"
"  padding-left: 6px;\n"
"}\n"
"QLabel#logo_2{\n"
"  background-color: #2b2b35;\n"
"  image: url(Ui/SideKick_Logo.png);\n"
"  width:100px;\n"
"  height:40px;\n"
"}\n"
"")
        self.side_menu.setObjectName("side_menu")
        self.dhsgd = QtWidgets.QVBoxLayout(self.side_menu)
        self.dhsgd.setContentsMargins(20, -1, 20, -1)
        self.dhsgd.setObjectName("dhsgd")
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.dhsgd.addItem(spacerItem6)
        self.logo_2 = QtWidgets.QLabel(self.side_menu)
        self.logo_2.setMinimumSize(QtCore.QSize(0, 50))
        self.logo_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.logo_2.setText("")
        self.logo_2.setObjectName("logo_2")
        self.dhsgd.addWidget(self.logo_2)
        spacerItem7 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.dhsgd.addItem(spacerItem7)
        self.boards_manager = QtWidgets.QPushButton(self.side_menu)
        self.boards_manager.setObjectName("boards_manager")
        self.dhsgd.addWidget(self.boards_manager)
        self.tune_actuators = QtWidgets.QPushButton(self.side_menu)
        self.tune_actuators.setObjectName("tune_actuators")
        self.dhsgd.addWidget(self.tune_actuators)
        self.baud_rate = QtWidgets.QComboBox(self.side_menu)
        self.baud_rate.setObjectName("baud_rate")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.baud_rate.addItem("")
        self.dhsgd.addWidget(self.baud_rate)
        self.supported_boards = QtWidgets.QComboBox(self.side_menu)
        self.supported_boards.setObjectName("supported_boards")
        self.dhsgd.addWidget(self.supported_boards)
        self.disconnect = QtWidgets.QPushButton(self.side_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disconnect.sizePolicy().hasHeightForWidth())
        self.disconnect.setSizePolicy(sizePolicy)
        self.disconnect.setObjectName("disconnect")
        self.dhsgd.addWidget(self.disconnect)
        self.selected_project = QtWidgets.QLabel(self.side_menu)
        self.selected_project.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.selected_project.setText("")
        self.selected_project.setAlignment(QtCore.Qt.AlignCenter)
        self.selected_project.setObjectName("selected_project")
        self.dhsgd.addWidget(self.selected_project)
        spacerItem8 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.dhsgd.addItem(spacerItem8)
        self.select_project = QtWidgets.QPushButton(self.side_menu)
        self.select_project.setObjectName("select_project")
        self.dhsgd.addWidget(self.select_project)
        self.new_project = QtWidgets.QPushButton(self.side_menu)
        self.new_project.setObjectName("new_project")
        self.dhsgd.addWidget(self.new_project)
        self.show_save = QtWidgets.QPushButton(self.side_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_save.sizePolicy().hasHeightForWidth())
        self.show_save.setSizePolicy(sizePolicy)
        self.show_save.setMinimumSize(QtCore.QSize(0, 0))
        self.show_save.setObjectName("show_save")
        self.dhsgd.addWidget(self.show_save)
        self.library_manager = QtWidgets.QPushButton(self.side_menu)
        self.library_manager.setObjectName("library_manager")
        self.dhsgd.addWidget(self.library_manager)
        self.arduino_cli = QtWidgets.QPushButton(self.side_menu)
        self.arduino_cli.setObjectName("arduino_cli")
        self.dhsgd.addWidget(self.arduino_cli)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dhsgd.addItem(spacerItem9)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dhsgd.addItem(spacerItem10)
        self.gridLayout.addWidget(self.side_menu, 1, 1, 5, 1)
        self.top_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_widget.sizePolicy().hasHeightForWidth())
        self.top_widget.setSizePolicy(sizePolicy)
        self.top_widget.setMinimumSize(QtCore.QSize(0, 100))
        self.top_widget.setObjectName("top_widget")
        self.gridLayout.addWidget(self.top_widget, 1, 5, 1, 2)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(5, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SideKick"))
        self.file.setText(_translate("MainWindow", "Menu"))
        self.device.setText(_translate("MainWindow", "Device"))
        self.upload.setText(_translate("MainWindow", "Upload"))
        self.compile.setText(_translate("MainWindow", "Compile"))
        self.record.setText(_translate("MainWindow", "Record"))
        self.help.setText(_translate("MainWindow", "Help"))
        self.quit.setText(_translate("MainWindow", "x"))
        self.full_screen.setText(_translate("MainWindow", "Expand"))
        self.debug_log.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Roboto \'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dfsssssssssssssssssssssssssshjdsbcjdsf</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">]#dsf</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dscvjkdszhvjkdsbvjhkdsv</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsviusdhjkdsgvhsfdbvouidsvsdvhioudsvnbjkdsbvhdsv</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">sdidsuhgvjdsbivuds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsvnbuidsjvds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">]vds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">vds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">v</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">ds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">vds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">]grsdvhisdjbvjhdsds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsvdsvhdsijgvbiusdbvuidsvs</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dviusdvghbuiedsbvuiysdbvuidsbv</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">sdvuiewsbvuidsbuvneds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">uidsvbikudsbvuierwbgfusddb fjkvl</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">vsdhouivdsbuidbfjkewsjsv</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">uoidsvbndsujkvbuoiebnvs</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">ihousdvkjsdbsa</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">bndjskvbjsd</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsvf</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsf</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">ds</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">f</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">dsf</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14px;\">fsdoikvnsjdkinbjkdsnvjldsnmfklds</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.boards_manager.setText(_translate("MainWindow", "Boards Manager"))
        self.tune_actuators.setText(_translate("MainWindow", "Tune Actuators"))
        self.baud_rate.setItemText(0, _translate("MainWindow", "115200"))
        self.baud_rate.setItemText(1, _translate("MainWindow", "57600"))
        self.baud_rate.setItemText(2, _translate("MainWindow", "38400"))
        self.baud_rate.setItemText(3, _translate("MainWindow", "9200"))
        self.disconnect.setText(_translate("MainWindow", "Disconnect"))
        self.select_project.setText(_translate("MainWindow", "Select Project"))
        self.new_project.setText(_translate("MainWindow", "New Project"))
        self.show_save.setText(_translate("MainWindow", "Show Save"))
        self.library_manager.setText(_translate("MainWindow", "Library Manager"))
        self.arduino_cli.setText(_translate("MainWindow", "Arduino CLI"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
