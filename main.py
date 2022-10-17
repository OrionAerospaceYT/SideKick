"""
This is the main python file responsible for having
the debugging window open.
This file also holds the
"""

from email import message
import sys
import threading
import time

import pyqtgraph as pg
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from torch import device

from device_manager import DeviceManager
from file_manager import FileManager
from message_handler import MessageHandler
from Ui.GraphingUi import Ui_MainWindow as graphing


class Graphing(qtw.QMainWindow):
    """
    Launches the main window (debugging window)
    """

    def __init__(self, parent=None):
        super(Graphing, self).__init__(parent=parent)

        self.main_ui = graphing()
        self.main_ui.setupUi(self)

        self.running = True
        self.supported_boards = {}

        self.top_legend = None
        self.top_plots = None
        self.main_ui_top_graph = None

        self.bottom_legend = None
        self.bottom_plots = None
        self.main_ui_bottom_graph = None

        self.get_supported_boards()

        self.map_top_graph()
        self.style_top_graph()

        self.map_bottom_graph()
        self.style_bottom_graph()

        self.connect_buttons()

        self.main_ui.project_name.setPlaceholderText("Enter projct name here.")
        self.main_ui.lineEdit.setPlaceholderText("Enter message here.")

        timer = qtc.QTimer(self)
        timer.setInterval(15)
        timer.timeout.connect(self.update)
        timer.start()

    def get_supported_boards(self):
        """
        gets all supported boards for the drop down option
        from the boards.csv file in the ./Ui directory
        """

        self.supported_boards = file_manager.get_all_boards()
        boards = list(self.supported_boards.keys())

        for board in boards:
            self.main_ui.device.addItem(board)

    def map_top_graph(self):
        """
        Set pyqtPlot to the top widget
        """

        self.main_ui_top_graph = pg.PlotWidget()
        self.main_ui_top_graph.setMenuEnabled(False)
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
        self.main_ui_bottom_graph.setMenuEnabled(False)
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
        self.main_ui.com_ports.activated[str].connect(
            event_handler.connect_device)
        self.main_ui.disconnect.clicked.connect(
            event_handler.disconnect_device)
        self.main_ui.record.clicked.connect(event_handler.record_data)

    def update_ports(self):
        """
        deals with updating the com ports that are avaliable on the GUI
        """

        gui_ports = [self.main_ui.com_ports.itemText(
            i) for i in range(self.main_ui.com_ports.count())]

        for port in event_handler.avaliable_port_list:
            if port not in gui_ports:
                self.main_ui.com_ports.addItem(port)

        for port in gui_ports:
            if port not in event_handler.avaliable_port_list:
                target = self.main_ui.com_ports.findText(port)
                self.main_ui.com_ports.removeItem(target)

    def update_projects(self):
        """
        deals with updating the projects avaliable in the SK Projects folder
        """

        gui_ports = [self.main_ui.project_paths.itemText(
            i) for i in range(self.main_ui.project_paths.count())]

        for project in event_handler.current_projects:
            if project not in gui_ports:
                self.main_ui.project_paths.addItem(project)

        for project in gui_ports:
            if project not in event_handler.current_projects:
                target = self.main_ui.project_paths.findText(project)
                self.main_ui.project_paths.removeItem(target)

    def turn_on_rec_light(self, is_on):
        """
        turns on or off the blinking record light
        """

        if is_on:
            self.main_ui.record.setStyleSheet("""image: url(Ui/Record.png);
                                                image-position: left;
                                                padding-left: 10px;
                                                width: 10px""")
        else:
            self.main_ui.record.setStyleSheet("")

    def update(self):
        """
        calls all update functions
        """

        self.update_ports()
        self.update_projects()
        message_handler.get_terminal_string(1)


class EventHandler():
    """
    This class deals with all events on the gui and connects
    them to python functions
    """

    def __init__(self):
        self.recording = False
        self.light_on = False

        self.avaliable_port_list = []
        self.current_projects = []
        self.supported_boards = []

        self.threaded_blinking_record = threading.Thread(
            target=self.blinking_record, args=(),)
        self.threaded_blinking_record.start()

        self.threaded_backend_loop = threading.Thread(
            target=self.threaded_backend, args=(),)
        self.threaded_backend_loop.start()

    def new_project(self):
        """
        creates the new project in the SK Projects folder
        sends a message to the screen if no name is entered or an invalid one
        sets the text of the project_name entry to ""
        """

        project_name = graphing.main_ui.project_name.text()
        if project_name == "":
            return
        if project_name in file_manager.get_all_projects():
            return

        file_manager.add_new_project(project_name)

        project_name = graphing.main_ui.project_name.setText("")

    def connect_device(self, port):
        """
        connects new devices through device manager and updates com port in
        message_handler
        """

        baud = graphing.main_ui.baud_rate.itemText(0)

        print(port, baud)

        if port == "Select COM":
            return

        device_manager.connect_device(port, baud)

    def disconnect_device(self):
        """
        disconnects the sidekick/teensy/arduino device
        """

        device_manager.terminate_device()

    def record_data(self):
        """
        blinks the record light and saves the data
        """

        # TODO
        self.recording = not self.recording

    def blinking_record(self):
        """
        the code associated with the blinking record light goes here
        """

        while SETTING_UP:
            pass

        while RUNNING:

            if not self.recording:
                graphing.turn_on_rec_light(True)

            if self.recording:
                graphing.turn_on_rec_light(self.light_on)
                self.light_on = not self.light_on

            # delay so that graphing is defined by the time the code runs
            time.sleep(1)

    def threaded_backend(self):
        """
        any code to be looped on a thread goes here
        waits until all variables are declared to loop
        """

        while SETTING_UP:
            pass

        while RUNNING:
            self.avaliable_port_list = device_manager.scan_avaliable_ports()
            self.current_projects = file_manager.get_all_projects()


RUNNING = True
SETTING_UP = True

device_manager = DeviceManager()
file_manager = FileManager()
event_handler = EventHandler()
message_handler = MessageHandler()

if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)

    with open("Ui/Style.css", "r", encoding="UTF-8") as style_sheet:
        app.setStyleSheet(style_sheet.read())

    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    graphing = Graphing()

    SETTING_UP = False

    graphing.show()
    app.exec_()

    RUNNING = False
