"""
This is the main python file responsible for having
the debugging window open.
This file also holds the
"""

import sys

import pyqtgraph as pg
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from device_manager import DeviceManager
from file_manager import FileManager
from Ui.GraphingUi import Ui_MainWindow as graphing


class Graphing(qtw.QMainWindow):
    """
    Launches the main window (debugging window)
    """

    def __init__(self, parent=None):
        super(Graphing, self).__init__(parent=parent)

        self.main_ui = graphing()
        self.main_ui.setupUi(self)

        self.top_legend = None
        self.top_plots = None
        self.main_ui_top_graph = None

        self.bottom_legend = None
        self.bottom_plots = None
        self.main_ui_bottom_graph = None

        self.map_top_graph()
        self.style_top_graph()

        self.map_bottom_graph()
        self.style_bottom_graph()

        self.connect_buttons()

        self.main_ui.project_name.setPlaceholderText("Enter projct name here.")

    def map_top_graph(self):
        """
        Set pyqtPlot to the top widget
        """

        self.main_ui_top_graph = pg.PlotWidget()
        self.main_ui.main_ui_top_graph = qtw.QVBoxLayout()

        self.main_ui.top_widget.setLayout(self.main_ui.main_ui_top_graph)
        self.main_ui.main_ui_top_graph.addWidget(self.main_ui_top_graph)
        self.top_legend = self.main_ui_top_graph.addLegend()
        self.top_plots = []

    def style_top_graph(self):
        """
        Sets the style for pyqtPlot top widget
        """

        self.main_ui_top_graph.setBackground('#32323C')
        self.top_legend.setLabelTextColor("#FFFFFF")
        self.main_ui_top_graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.main_ui_top_graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.main_ui_top_graph.getAxis("left").setTextPen((255, 255, 255))
        self.main_ui_top_graph.getAxis("bottom").setTextPen((255, 255, 255))

    def map_bottom_graph(self):
        """
        Set pyqtPlot lib to the bottom widget
        """

        self.main_ui_bottom_graph = pg.PlotWidget()
        self.main_ui.main_ui_bottom_graph = qtw.QVBoxLayout()

        self.main_ui.bottom_widget.setLayout(
            self.main_ui.main_ui_bottom_graph)
        self.main_ui.main_ui_bottom_graph.addWidget(
            self.main_ui_bottom_graph)
        self.bottom_legend = self.main_ui_bottom_graph.addLegend()
        self.bottom_plots = []

    def style_bottom_graph(self):
        """
        Sets the style for pyqtPlot bottom widget
        """

        self.main_ui_bottom_graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.main_ui_bottom_graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.main_ui_bottom_graph.setBackground('#32323C')
        self.bottom_legend.setLabelTextColor("#FFFFFF")
        self.main_ui_bottom_graph.getAxis("left").setTextPen((255, 255, 255))
        self.main_ui_bottom_graph.getAxis(
            "bottom").setTextPen((255, 255, 255))

    def connect_buttons(self):
        """
        Connects the buttons on the gui to python functions
        """

        self.main_ui.render.setDisabled(True)
        self.main_ui.new_project.clicked.connect(event_handler.new_project)


class EventHandler():
    """
    This class deals with all events on the gui and connects
    them to python functions
    """

    def __init__(self):
        self.i = 0

    def new_project(self):
        """
        creates the new project in the SK Projects folder
        sends a message to the screen if no name is entered or an invalid one
        sets the text of the project_name entry to ""
        """

        project_name = graphing.main_ui.project_name.text()
        if project_name == "":
            print(project_name)
        if project_name in file_manager.get_all_projects():
            print(project_name)

        project_name = graphing.main_ui.project_name.setText("")


device_manager = DeviceManager()
file_manager = FileManager()
event_handler = EventHandler()

if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)

    with open("Ui/Style.css", "r", encoding="UTF-8") as style_sheet:
        app.setStyleSheet(style_sheet.read())

    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    graphing = Graphing()
    graphing.show()
    app.exec_()
