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
from Ui.GraphingUi import Ui_MainWindow as main_window


class MainGUI(qtw.QMainWindow):
    """
    Launches the main window (debugging window)

    this class inherits QMainWindow from PyQt5.QtWidgets as
    it holds the gui object which we need to modify.
    """

    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent=parent)

        # Definitions for gui initialisation go here

        self.main_ui = main_window()
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
        self.connect_keyboard_shortcuts()

        self.main_ui.project_name.setPlaceholderText("Enter projct name here.")
        self.main_ui.message.setPlaceholderText("Enter message here.")

        self.main_ui.bottom_update.setAlignment(
            Qt.AlignRight | Qt.AlignVCenter)

        self.add_supported_boards()

        # Definitions for event handling goes here

        self.recording = False
        self.light_on = False
        self.file_manager = False
        self.device_manager = False
        self.debug_window = False
        self.prev_debug_window = True
        self.upload = False
        self.compile = False

        self.commands = []

        self.avaliable_port_list = []
        self.current_projects = []
        self.supported_boards = []

        threaded_blinking_record = threading.Thread(
            target=self.blinking_record, args=(),)
        threaded_blinking_record.start()

        threaded_backend_loop = threading.Thread(
            target=self.threaded_backend, args=(),)
        threaded_backend_loop.start()

        self.board, self.project = file_manager.load_options()

        self.main_ui.supported_boards.setCurrentText(self.board)
        self.main_ui.select_project.setCurrentText(self.project)

        timer = qtc.QTimer(self)
        timer.setInterval(15)
        timer.timeout.connect(self.update)
        timer.start()

    def add_supported_boards(self):
        """
        Adds the supported boards to the drop down so that
        they can be selected for uploads.
        """

        boards = list(file_manager.get_all_boards().keys())

        for board in boards:

            self.main_ui.supported_boards.addItem(board)

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

        self.main_ui_top_graph.setBackground('#2b2b35')
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
        self.main_ui_bottom_graph.setBackground('#2b2b35')
        self.bottom_legend.setLabelTextColor("#FFFFFF")
        self.main_ui_bottom_graph.getAxis("left").setTextPen((255, 255, 255))
        self.main_ui_bottom_graph.getAxis(
            "bottom").setTextPen((255, 255, 255))

    def connect_buttons(self):
        """
        Connects the buttons/drop-downs on the gui to python functions
        """

        self.main_ui.record.clicked.connect(self.record_data)
        self.main_ui.file.clicked.connect(self.open_file_manager)
        self.main_ui.device.clicked.connect(self.open_device_manager)
        self.main_ui.new_project.clicked.connect(self.new_project)
        self.main_ui.upload.clicked.connect(self.upload_project)
        self.main_ui.quit.clicked.connect(self.close_debug_window)
        self.main_ui.message.returnPressed.connect(self.send)
        self.main_ui.compile.clicked.connect(self.compile_project)
        self.main_ui.com_ports.activated[str].connect(self.connect_device)
        self.main_ui.disconnect.clicked.connect(self.disconnect_device)

        self.main_ui.select_project.activated[str].connect(
            self.open_file_manager)

    def connect_keyboard_shortcuts(self):
        """
        Connects keyboard shortcuts to their respective functions:
            ctrl + x (disconnect)
            ctrl + s (verify/compile)
            ctrl + u (upload)
            ctrl + r (record)
            ctrl + h (help)
        """

        disconnect = qtw.QShortcut(qtg.QKeySequence("ctrl+x"), self)
        disconnect.activated.connect(self.disconnect_device)

        compile_code = qtw.QShortcut(qtg.QKeySequence("ctrl+s"), self)
        compile_code.activated.connect(self.compile_project)

        upload = qtw.QShortcut(qtg.QKeySequence("ctrl+u"), self)
        upload.activated.connect(self.upload_project)

        record = qtw.QShortcut(qtg.QKeySequence("ctrl+r"), self)
        record.activated.connect(self.record_data)

        help_website = qtw.QShortcut(qtg.QKeySequence("ctrl+h"), self)
        help_website.activated.connect(self.demo_function)

    def turn_on_rec_light(self, is_on):
        """
        Turns on or off the blinking record light

        Args:
            is_on (boolean): either shows or hides the record light
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
        for project in self.current_projects:
            if project not in projects_on_gui:
                self.main_ui.select_project.addItem(project)
        for project in projects_on_gui:
            if project not in self.current_projects:
                target = self.main_ui.select_project.findText(project)
                self.main_ui.select_project.removeItem(target)

    def update_ports(self):
        """
        Updates all avaliable ports, removes unavaliable one
        """

        ports_on_gui = [self.main_ui.com_ports.itemText(
            i) for i in range(self.main_ui.com_ports.count())]
        for port in self.avaliable_port_list:
            if port not in ports_on_gui:
                self.main_ui.com_ports.addItem(port)
        for port in ports_on_gui:
            if port not in self.avaliable_port_list:
                target = self.main_ui.com_ports.findText(port)
                self.main_ui.com_ports.removeItem(target)

    def update(self):
        """
        calls all update functions
        """

        self.update_ports()
        self.update_projects()

        if self.prev_debug_window != self.debug_window:
            if self.debug_window:
                self.main_ui.debugger.setVisible(True)
                self.main_ui.debug_log.setHtml(message_handler.debug_html)
            else:
                self.main_ui.debugger.setVisible(False)

        if self.compile:
            self.main_ui.top_update.setText(
                message_handler.get_status("Compiling"))
        elif self.upload:
            self.main_ui.top_update.setText(
                message_handler.get_status("Uploading"))
        else:
            self.main_ui.top_update.setText("")

        if self.device_manager:
            self.main_ui.device_layout.setVisible(True)
            self.main_ui.file_layout.setVisible(False)
        elif self.file_manager:
            self.main_ui.file_layout.setVisible(True)
            self.main_ui.device_layout.setVisible(False)
        else:
            self.main_ui.file_layout.setVisible(False)
            self.main_ui.device_layout.setVisible(False)

        self.main_ui.terminal.setHtml(message_handler.terminal_html)

        if device_manager.port is not None:
            self.main_ui.bottom_update.setText("Connected")
        else:
            self.main_ui.bottom_update.setText("Not Connected")

        self.prev_debug_window = self.debug_window

        if device_manager.port is not None:

            self.main_ui.com_ports.setCurrentText(device_manager.port)

    def new_project(self):
        """
        creates the new project in the SK Projects folder
        sends a message to the screen if no name is entered or an invalid one
        sets the text of the project_name entry to ""
        """

        project_name = self.main_ui.project_name.text()
        if project_name == "":
            return
        if project_name in file_manager.get_all_projects():
            return

        file_manager.add_new_project(project_name)

        project_name = self.main_ui.project_name.setText("")

    def connect_device(self, port):
        """
        Connects new devices through device manager and updates com port in
        message_handler

        Args:
            port (string): the com port selected in the gui
        """

        baud = self.main_ui.baud_rate.itemText(0)

        device_manager.connect_device(port, baud)

    def send(self):
        """
        Sends the message from the line edit to the connected device
        """

        device_manager.send(self.main_ui.message.text())

        self.main_ui.message.setText("")

    def disconnect_device(self):
        """
        Disconnects the sidekick/teensy/arduino device
        """

        device_manager.terminate_device()

    def record_data(self):
        """
        Blinks the record light and saves the data
        """

        self.recording = not self.recording

    def open_file_manager(self):
        """
        Opens/closes the file menu
        Closes device manager if they are both open at the same time
        """

        self.file_manager = not self.file_manager

        if self.device_manager and self.file_manager:
            self.device_manager = False

    def open_device_manager(self):
        """
        Opens/closes the device menu
        Closes file manager if they are both open at the same time
        """

        self.device_manager = not self.device_manager

        if self.device_manager and self.file_manager:
            self.file_manager = False

    def upload_project(self):
        """
        TODO:

        Gets selected board to upload to
        Checks if a device is connected to the gui
        Disconnects the device to upload
        Compiles the script and then uploads the script
        Reconnects the device - or - Displays error on the screen
        """

        project = self.main_ui.select_project.currentText()
        boards_dictionary = file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = device_manager.port

        self.commands = file_manager.compile_and_upload_commands(
            port, project, board)

        self.upload = True

    def compile_project(self):
        """
        Compiles the script
        """

        project = self.main_ui.select_project.currentText()
        boards_dictionary = file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = device_manager.port

        self.commands = file_manager.compile_and_upload_commands(
            port, project, board)

        self.compile = True

    def close_debug_window(self):
        """
        Closes the bottom pop up layout
        """

        self.debug_window = False

    def demo_function(self):
        """
        Prints "Hello world!"
        Used to demo connected buttons
        """
        print("Hello world!")

    def blinking_record(self):
        """
        Non-blocking function to perform functions over a time interval
        """

        while RUNNING:
            if not self.recording:
                self.turn_on_rec_light(True)

            if self.recording:
                self.turn_on_rec_light(self.light_on)
                self.light_on = not self.light_on

            if self.compile:
                message_handler.update_ellipsis()
            if self.upload:
                message_handler.update_ellipsis()

            time.sleep(0.5)

    def threaded_backend(self):
        """
        All backend tasks that need to be performed continually
        """

        while RUNNING:
            port = device_manager.port
            self.avaliable_port_list = device_manager.scan_avaliable_ports(
                port)
            self.current_projects = file_manager.get_all_projects()
            message_handler.raw_data = device_manager.raw_data

            message_handler.terminal_output_html(
                self.main_ui.terminal.height())

            if self.compile:
                self.debug_window = False

                error = device_manager.compile_script(self.commands[0])
                message_handler.decode_debug_message(error)

                self.debug_window = True
                self.compile = False

            if self.upload:

                self.debug_window = False

                port = device_manager.port
                device_manager.terminate_device()

                error, success = device_manager.upload_script(
                    self.commands[0], self.commands[1])

                if not success:
                    message_handler.decode_debug_message(error)
                    self.debug_window = True

                time.sleep(0.25)
                self.connect_device(port)

                self.upload = False


device_manager = DeviceManager()
file_manager = FileManager()
message_handler = MessageHandler()

RUNNING = True

if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)
    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    main_gui = MainGUI()

    main_gui.show()
    app.exec_()

    device_manager.terminate_device()
    RUNNING = False

    project_selected = main_gui.main_ui.select_project.currentText()
    board_selected = main_gui.main_ui.supported_boards.currentText()

    file_manager.save_options(board_selected, project_selected)
