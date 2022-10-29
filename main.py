"""
This is the main python file responsible for having
the debugging window open.
This file also holds the
"""

import sys
import threading
import time

import pyqtgraph as pg
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt

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

        self.menu_width = 0
        self.running = True
        self.supported_boards = {}

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
        self.main_ui.message.setPlaceholderText("Enter message here.")

        self.main_ui.bottom_update.setAlignment(Qt.AlignRight)
        self.main_ui.upload.setMinimumWidth(80)
        self.main_ui.help.setMinimumWidth(80)

        timer = qtc.QTimer(self)
        timer.setInterval(15)
        timer.timeout.connect(self.update)
        timer.start()

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

        self.main_ui.record.clicked.connect(event_handler.record_data)
        self.main_ui.file.clicked.connect(event_handler.open_file_manager)
        self.main_ui.device.clicked.connect(event_handler.open_device_manager)
        self.main_ui.new_project.clicked.connect(event_handler.new_project)

        self.main_ui.message.returnPressed.connect(event_handler.send)

        self.main_ui.select_project.activated[str].connect(
            event_handler.open_file_manager)

        self.main_ui.com_ports.activated[str].connect(
            event_handler.connect_device)

        self.main_ui.disconnect.clicked.connect(
            event_handler.disconnect_device)

    def turn_on_rec_light(self, is_on):
        """
        turns on or off the blinking record light
        """

        if is_on:
            self.main_ui.record_light.setStyleSheet("""image: url(Ui/Record.png);
                                                    image-position: center;
                                                    """)
        else:
            self.main_ui.record_light.setStyleSheet("")

    def update_projects(self):
        """
        Updates the current projects window so it shows all projects in the project folder.
        """

        projects_on_gui = [self.main_ui.select_project.itemText(
            i) for i in range(self.main_ui.select_project.count())]
        for project in event_handler.current_projects:
            if project not in projects_on_gui:
                self.main_ui.select_project.addItem(project)
        for project in projects_on_gui:
            if project not in event_handler.current_projects:
                target = self.main_ui.select_project.findText(project)
                self.main_ui.select_project.removeItem(target)

    def update_ports(self):
        """
        Updates all avaliable ports, removes unavaliable one
        """

        ports_on_gui = [self.main_ui.com_ports.itemText(
            i) for i in range(self.main_ui.com_ports.count())]
        for port in event_handler.avaliable_port_list:
            if port not in ports_on_gui:
                self.main_ui.com_ports.addItem(port)
        for port in ports_on_gui:
            if port not in event_handler.avaliable_port_list:
                target = self.main_ui.com_ports.findText(port)
                self.main_ui.com_ports.removeItem(target)

    def update(self):
        """
        calls all update functions
        """

        self.update_ports()
        self.update_projects()

        if self.menu_width == 0:
            self.main_ui.file_layout.setVisible(False)
            self.main_ui.device_layout.setVisible(False)
        elif event_handler.device_manager:
            self.main_ui.device_layout.setVisible(True)
            self.main_ui.device_layout.setMinimumWidth(self.menu_width)
            self.main_ui.file_layout.setVisible(False)
        elif event_handler.file_manager:
            self.main_ui.file_layout.setVisible(True)
            self.main_ui.file_layout.setMinimumWidth(self.menu_width)
            self.main_ui.device_layout.setVisible(False)

        self.main_ui.terminal.setHtml(message_handler.terminal_html)

        if device_manager.port is not None:
            self.main_ui.bottom_update.setText(
                "Connected: " + device_manager.port)
        else:
            self.main_ui.bottom_update.setText("Not Connected")


class EventHandler():
    """
    This class deals with all events on the gui and connects
    them to python functions
    """

    def __init__(self):
        self.recording = False
        self.light_on = False
        self.file_manager = False
        self.device_manager = False

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

        if port == "Select COM":
            return

        device_manager.connect_device(port, baud)

    def send(self):
        """
        sends the message from the line edit to the connected device
        """

        device_manager.send(graphing.main_ui.message.text())

        graphing.main_ui.message.setText("")

    def disconnect_device(self):
        """
        disconnects the sidekick/teensy/arduino device
        """

        device_manager.terminate_device()

    def record_data(self):
        """
        blinks the record light and saves the data
        """

        self.recording = not self.recording

    def open_file_manager(self):
        """
        opens/closes the file menu
        also closes device manager if they are both open at the same time
        """

        self.file_manager = not self.file_manager

        if self.device_manager and self.file_manager:
            self.device_manager = False

    def open_device_manager(self):
        """
        opens/closes the device menu
        also closes file manager if they are both open at the same time
        """

        self.device_manager = not self.device_manager

        if self.device_manager and self.file_manager:
            self.file_manager = False

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

            time.sleep(0.5)

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
            message_handler.raw_data = device_manager.raw_data

            message_handler.terminal_output_html(
                graphing.main_ui.terminal.height())

            if not self.file_manager and not self.device_manager:
                graphing.menu_width = 0
            else:
                graphing.menu_width = int(
                    (graphing.main_ui.top_bar.width() / 3)) - 50


RUNNING = True
SETTING_UP = True

device_manager = DeviceManager()
file_manager = FileManager()
event_handler = EventHandler()
message_handler = MessageHandler()

if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)
    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    graphing = Graphing()

    SETTING_UP = False

    graphing.show()
    app.exec_()

    # Stops all threads from running at program quit
    RUNNING = False
    device_manager.terminate_device()
