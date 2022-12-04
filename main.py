"""
This is the main python file responsible for having
the debugging window open.
This file also holds the

TODO fix teensy upload (auto upload mode)
TODO make classes for device manager window and file manager winow
TODO display COM by default in COM dropdown
"""

import sys
import threading
import time

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt

from device_manager import DeviceManager
from file_manager import FileManager
#from widgets import DeviceManagerWindow
#rom widgets import FileManagerWindow
from widgets import Graph
from message_handler import MessageHandler
from Ui.GraphingUi import Ui_MainWindow as main_window


class MainGUI(qtw.QMainWindow):
    """
    Launches the main window (debugging window)

    This class inherits QMainWindow from PyQt5.QtWidgets as
    it holds the gui object which we need to modify.

    This class also usues the Graph class from graphs.py
    """

    def __init__(self):

        super(MainGUI, self).__init__()

        # Attributes for the gui are defined here
        self.device_manager = DeviceManager()
        self.file_manager = FileManager()
        self.message_handler = MessageHandler()

        self.main_ui = main_window()
        self.main_ui.setupUi(self)

        self.menu_width = 0
        self.supported_boards = {}

        self.top_graph = Graph(key="1")
        self.main_ui.top_graph = qtw.QVBoxLayout()
        self.main_ui.top_graph.addWidget(self.top_graph.graph)
        self.main_ui.top_widget.setLayout(self.main_ui.top_graph)

        self.bottom_graph = Graph(key="2")
        self.main_ui.bottom_graph = qtw.QVBoxLayout()
        self.main_ui.bottom_graph.addWidget(self.bottom_graph.graph)
        self.main_ui.bottom_widget.setLayout(self.main_ui.bottom_graph)

        self.connect_buttons()
        self.connect_keyboard_shortcuts()
        self.main_ui.project_name.setPlaceholderText("Enter projct name here.")
        self.main_ui.message.setPlaceholderText("Enter message here.")
        self.main_ui.bottom_update.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.add_supported_boards()

        # Attributes for event handling are defined here
        self.recording = False
        self.light_on = False
        self.file_manager_window = False
        self.device_manager_window = False
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

        self.board, self.project = self.file_manager.load_options()

        self.main_ui.supported_boards.setCurrentText(self.board)
        self.main_ui.select_project.setCurrentText(self.project)

        timer = qtc.QTimer(self)
        timer.setInterval(25)
        timer.timeout.connect(self.update)
        timer.start()

    def add_supported_boards(self):
        """main_ui_top_graph
        Adds the supported boards to the drop down so that
        they can be selected for uploads.
        """

        boards = list(self.file_manager.get_all_boards().keys())

        for board in boards:

            self.main_ui.supported_boards.addItem(board)

    def connect_buttons(self):
        """
        Connects the buttons/drop-downs on the gui to python functions
        """

        self.main_ui.record.clicked.connect(self.record_data)
        self.main_ui.file.clicked.connect(self.open_file_manager)
        self.main_ui.device.clicked.connect(self.open_device_manager)
        self.main_ui.project_name.returnPressed.connect(self.new_project)
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
        self.top_graph.update_graph()
        self.bottom_graph.update_graph()

        if self.prev_debug_window != self.debug_window:
            if self.debug_window:
                self.main_ui.debugger.setVisible(True)
                self.main_ui.debug_log.setHtml(self.message_handler.debug_html)
            else:
                self.main_ui.debugger.setVisible(False)

        if self.compile:
            self.main_ui.top_update.setText(
                self.message_handler.get_status("Compiling"))
        elif self.upload:
            self.main_ui.top_update.setText(
                self.message_handler.get_status("Uploading"))
        else:
            self.main_ui.top_update.setText("")

        if self.device_manager_window:
            self.main_ui.device_layout.setVisible(True)
            self.main_ui.file_layout.setVisible(False)
        elif self.file_manager_window:
            self.main_ui.file_layout.setVisible(True)
            self.main_ui.device_layout.setVisible(False)
        else:
            self.main_ui.file_layout.setVisible(False)
            self.main_ui.device_layout.setVisible(False)

        self.main_ui.terminal.setHtml(self.message_handler.terminal_html)

        if self.device_manager.port is not None:
            self.main_ui.bottom_update.setText("Connected")
        else:
            self.main_ui.bottom_update.setText("Not Connected")

        self.prev_debug_window = self.debug_window

        if self.device_manager.port is not None:

            self.main_ui.com_ports.setCurrentText(self.device_manager.port)

    def new_project(self):
        """
        creates the new project in the SK Projects folder
        sends a message to the screen if no name is entered or an invalid one
        sets the text of the project_name entry to ""
        """

        project_name = self.main_ui.project_name.text()
        if project_name == "":
            return
        if project_name in self.file_manager.get_all_projects():
            return

        self.file_manager.add_new_project(project_name)

        project_name = self.main_ui.project_name.setText("")

    def connect_device(self, port):
        """
        Connects new devices through device manager and updates com port in
        self.message_handler

        Args:
            port (string): the com port selected in the gui
        """

        baud = self.main_ui.baud_rate.itemText(0)

        self.device_manager.connect_device(port, baud)

    def send(self):
        """
        Sends the message from the line edit to the connected device
        """

        self.device_manager.send(self.main_ui.message.text())

        self.main_ui.message.setText("")

    def disconnect_device(self):
        """
        Disconnects the sidekick/teensy/arduino device
        """

        self.device_manager.terminate_device()

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

        self.file_manager_window = not self.file_manager_window

        if self.device_manager_window and self.file_manager_window:
            self.device_manager_window = False

    def open_device_manager(self):
        """
        Opens/closes the device menu
        Closes file manager if they are both open at the same time
        """

        self.device_manager_window = not self.device_manager_window

        if self.device_manager_window and self.file_manager_window:
            self.file_manager_window = False

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
        boards_dictionary = self.file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = self.device_manager.port

        self.commands = self.file_manager.compile_and_upload_commands(
            port, project, board)

        self.upload = True

    def compile_project(self):
        """
        Compiles the script
        """

        project = self.main_ui.select_project.currentText()
        boards_dictionary = self.file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = self.device_manager.port

        self.commands = self.file_manager.compile_and_upload_commands(
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
                self.message_handler.update_ellipsis()
            if self.upload:
                self.message_handler.update_ellipsis()

            time.sleep(0.5)

    def threaded_backend(self):
        """
        All backend tasks that need to be performed continually
        """

        while RUNNING:
            # Com ports
            port = self.device_manager.port
            self.avaliable_port_list = self.device_manager.scan_avaliable_ports(port)

            # Projects
            self.current_projects = self.file_manager.get_all_projects()

            # Raw data
            raw_data = self.device_manager.raw_data

            size = (self.main_ui.terminal.height(), self.main_ui.terminal.width())

            self.message_handler.get_terminal(raw_data, size)
            self.top_graph.set_graph_data(raw_data)
            self.bottom_graph.set_graph_data(raw_data)

            if self.compile:
                self.debug_window = False

                error = self.device_manager.compile_script(self.commands[0])
                self.message_handler.decode_debug_message(error)

                self.debug_window = True
                self.compile = False

            if self.upload:

                self.debug_window = False

                port = self.device_manager.port
                self.device_manager.terminate_device()

                error, success = self.device_manager.upload_script(
                    self.commands[0], self.commands[1])

                if not success:
                    self.message_handler.decode_debug_message(error)
                    self.debug_window = True

                time.sleep(0.25)
                self.connect_device(port)

                self.upload = False

if __name__ == "__main__":

    RUNNING = True

    app = qtw.QApplication(sys.argv)
    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    main_gui = MainGUI()

    main_gui.show()
    app.exec_()

    main_gui.device_manager.terminate_device()
    RUNNING = False

    project_selected = main_gui.main_ui.select_project.currentText()
    board_selected = main_gui.main_ui.supported_boards.currentText()

    main_gui.file_manager.save_options(board_selected, project_selected)
