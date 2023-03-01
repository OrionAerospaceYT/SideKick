"""
This is the main python file responsible for having
the debugging window open.
This file also holds the

TODO fix teensy upload (auto upload mode)
TODO make classes for device manager window and file manager winow
TODO display COM by default in COM dropdown
TODO loading saved data (GUI re design in file manager)
"""

import sys
import threading
import time
import webbrowser

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw

from actuator import ActuatorGUI
from library import LibraryManager
from device_manager import DeviceManager
from file_manager import FileManager

from widgets import Graph
from widgets import RecordLight
from widgets import SideMenu

from message_handler import MessageHandler
from Ui.GraphingUi import Ui_MainWindow as main_window

DEV = False
CONSCIOS_PATH = "C:\\Users\\a-armitage17\\Documents\\GitHub\\SideKick\\ConsciOS"

class MainGUI(qtw.QMainWindow):
    """
    Launches the main window (debugging window)

    This class inherits QMainWindow from PyQt5.QtWidgets as
    it holds the gui object which we need to modify.

    This class also usues the Graph class from graphs.py

    Args:
        qtw (QtWidgets): the main window functions
    """

    def __init__(self):

        super().__init__()

        self.main_ui = main_window()
        self.main_ui.setupUi(self)

        # Associative classes are initialised here
        self.device_manager = DeviceManager()
        self.file_manager = FileManager(DEV, CONSCIOS_PATH)
        self.top_graph = Graph(key="1")
        self.bottom_graph = Graph(key="2")
        self.message_handler = MessageHandler()
        self.record_light = RecordLight()
        self.side_menu = SideMenu(
            self.file_and_device_widgets()[0],
            self.file_and_device_widgets()[1],
            self.main_ui.side_menu)

        # Attributes and initial config here
        self.side_menu.hide_menu()

        self.main_ui.top_graph = qtw.QVBoxLayout()
        self.main_ui.top_graph.addWidget(self.top_graph.graph)
        self.main_ui.top_widget.setLayout(self.main_ui.top_graph)

        self.main_ui.bottom_graph = qtw.QVBoxLayout()
        self.main_ui.bottom_graph.addWidget(self.bottom_graph.graph)
        self.main_ui.bottom_widget.setLayout(self.main_ui.bottom_graph)

        self.connect_buttons()
        self.connect_keyboard_shortcuts()
        self.main_ui.message.setPlaceholderText("Enter message here.")
        self.main_ui.bottom_update.setAlignment(qtc.Qt.AlignRight | qtc.Qt.AlignVCenter)
        self.add_supported_boards()

        # Attributes for event handling are defined here
        self.debug_window = False
        self.prev_debug_window = True
        self.showing_data = False
        self.upload = False
        self.compile = False

        self.commands = []
        self.avaliable_port_list = []
        self.current_projects = []
        self.supported_boards = []
        self.current_saves = []

        self.supported_boards = {}

        threaded_blinking_record = threading.Thread(
            target=self.record_light.threaded_blink, args=(),)
        threaded_blinking_record.start()

        threaded_backend_loop = threading.Thread(
            target=self.threaded_backend, args=(),)
        threaded_backend_loop.start()

        board, project = self.file_manager.load_options()

        self.main_ui.supported_boards.setCurrentText(board)
        self.file_manager.current_project = project

        timer = qtc.QTimer(self)
        timer.setInterval(25)
        timer.timeout.connect(self.update)
        timer.start()

    def file_and_device_widgets(self):
        """
        Connects all of the buttons and other widgets
        to the side menu class

        Returns:
            list: the list of file manager widgets
            list: the list of device manager widgets
        """
        file_manager = [self.main_ui.selected_project,
                        self.main_ui.select_project,
                        self.main_ui.new_project,
                        self.main_ui.show_save,
                        self.main_ui.library_manager]

        device_manager = [self.main_ui.tune_actuators,
                          self.main_ui.baud_rate,
                          self.main_ui.disconnect,
                          self.main_ui.supported_boards]

        return file_manager, device_manager

    def open_library_manager(self):
        """
        Opens the library manager window
        """
        LibraryManager(self.file_manager, self)

    def open_actuator_gui(self):
        """
        Opens the actuator tuning suite
        """

        self.upload_project()
        ActuatorGUI(self.device_manager, self)

    def add_supported_boards(self):
        """
        main_ui_top_graph
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

        self.main_ui.record.clicked.connect(self.record_light.update_recording)
        self.main_ui.file.clicked.connect(self.open_file_manager)
        self.main_ui.device.clicked.connect(self.open_device_manager)
        self.main_ui.upload.clicked.connect(self.upload_project)
        self.main_ui.quit.clicked.connect(self.close_debug_window)
        self.main_ui.compile.clicked.connect(self.compile_project)
        self.main_ui.disconnect.clicked.connect(self.device_manager.terminate_device)
        self.main_ui.library_manager.clicked.connect(self.open_library_manager)
        self.main_ui.show_save.clicked.connect(self.display_save)
        self.main_ui.message.returnPressed.connect(self.send)
        self.main_ui.select_project.clicked.connect(self.open_file)
        self.main_ui.new_project.clicked.connect(self.new_project)
        self.main_ui.help.clicked.connect(self.show_help)
        self.main_ui.com_ports.activated[str].connect(self.connect_device)
        self.main_ui.tune_actuators.clicked.connect(self.open_actuator_gui)

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
        disconnect.activated.connect(self.device_manager.terminate_device)

        compile_code = qtw.QShortcut(qtg.QKeySequence("ctrl+s"), self)
        compile_code.activated.connect(self.compile_project)

        upload = qtw.QShortcut(qtg.QKeySequence("ctrl+u"), self)
        upload.activated.connect(self.upload_project)

        record = qtw.QShortcut(qtg.QKeySequence("ctrl+r"), self)
        record.activated.connect(self.record_light.update_recording)

        help_website = qtw.QShortcut(qtg.QKeySequence("ctrl+h"), self)
        help_website.activated.connect(self.demo_function)

        tune_actuators = qtw.QShortcut(qtg.QKeySequence("ctrl+a"), self)
        tune_actuators.activated.connect(self.open_actuator_gui)

    def turn_on_rec_light(self, is_on):
        """
        Turns on or off the blinking record light

        Args:
            is_on (boolean): either shows or hides the record light
        """

        if is_on:
            self.main_ui.record_light.setStyleSheet("""image: url(Ui/Record.png);
                                                    image-position: center;""")
        else:
            self.main_ui.record_light.setStyleSheet("")

    def update_compile_and_upload(self):
        """
        Updates the top label while uploading or compiling
        """

        if self.compile:
            self.main_ui.top_update.setStyleSheet("QLabel{font-size:14pt}")
            self.main_ui.top_update.setText(
                self.message_handler.get_status("Compiling"))
        elif self.upload:
            self.main_ui.top_update.setStyleSheet("QLabel{font-size:14pt}")
            self.main_ui.top_update.setText(
                self.message_handler.get_status("Uploading"))
        elif self.device_manager.error is not None:
            self.main_ui.top_update.setStyleSheet("QLabel{font-size:10pt}")
            self.main_ui.top_update.setText(
                f"Error, could not connect!\n{self.device_manager.error}")
        else:
            self.main_ui.top_update.setStyleSheet("QLabel{font-size:14pt}")
            self.main_ui.top_update.setText("")

    def update_ports(self):
        """
        Updates all avaliable ports, removes unavaliable ones
        """
        ports_on_gui = [self.main_ui.com_ports.itemText(
            i) for i in range(self.main_ui.com_ports.count())]

        # adds new items
        for port in self.avaliable_port_list:
            if port not in ports_on_gui:
                self.main_ui.com_ports.addItem(port)

        # removes old items
        for port in ports_on_gui:
            if port not in self.avaliable_port_list:
                target = self.main_ui.com_ports.findText(port)
                self.main_ui.com_ports.removeItem(target)

    def update_terminal(self):
        """
        updates the html of the terminal
        """
        self.main_ui.terminal.setHtml(self.message_handler.terminal_html)

    def update(self):
        """
        calls all update functions
        """

        # set labels
        name = self.file_manager.parsed_project_name()
        if name:
            self.main_ui.selected_project.setText(name)
        else:
            self.main_ui.selected_project.setText("Select A Project!")

        # update functions
        self.update_ports()
        self.top_graph.update_graph()
        self.bottom_graph.update_graph()

        # debugging window
        if self.prev_debug_window != self.debug_window:
            if self.debug_window:
                self.main_ui.debugger.setVisible(True)
                self.main_ui.debug_log.setHtml(self.message_handler.debug_html)
            else:
                self.main_ui.debugger.setVisible(False)
        self.prev_debug_window = self.debug_window

        # record light
        self.turn_on_rec_light(self.record_light.show)

        self.update_compile_and_upload()

        if (self.device_manager.connected) or (not self.showing_data):
            self.main_ui.terminal.setHtml(self.message_handler.terminal_html)


        if self.device_manager.connected:
            self.main_ui.bottom_update.setText("Connected")
            self.main_ui.com_ports.setCurrentText(self.device_manager.port)
        else:
            self.main_ui.bottom_update.setText("Not Connected")

    def new_project(self):
        """
        Gets the directory URL from getExistingDirectoryUrl with a
        QFileDialog and then creates a sidekick project in that directory.
        TODO
        """
        folder_path = qtw.QFileDialog.getSaveFileName(self,
                            'Create Folder', self.file_manager.projects_path, 'Folders (*)')[0]

        if folder_path:
            self.file_manager.add_new_project(folder_path)

    def connect_device(self, port):
        """
        Connects new devices through device manager and updates com por[t in
        self.message_handler

        Args:
            port (string): the com port selected in the gui
        """

        baud = self.main_ui.baud_rate.itemText(0)
        if DEV and port == "emulate":
            self.device_manager.connect_device(port, baud, dev=True)
        else:
            self.device_manager.connect_device(port, baud)

    def send(self):
        """
        Sends the message from the line edit to the connected device
        """

        self.device_manager.send(self.main_ui.message.text())

        self.main_ui.message.setText("")

    def open_file_manager(self):
        """
        Opens/closes the file menu
        Closes device manager if they are both open at the same time
        """

        self.side_menu.show_side_menu(file=True)

    def open_device_manager(self):
        """
        Opens/closes the device menu
        Closes file manager if they are both open at the same time
        """

        self.side_menu.show_side_menu(device=True)

    def upload_project(self):
        """
        Gets selected board to upload to
        Checks if a device is connected to the gui
        Disconnects the device to upload
        Compiles the script and then uploads the script
        Reconnects the device - or - Displays error on the screen
        """

        boards_dictionary = self.file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = self.device_manager.port

        self.file_manager.set_current_project("", manual=True)
        self.commands = self.file_manager.compile_and_upload_commands(port, board)

        self.upload = True

    def compile_project(self):
        """
        Compiles the script
        """

        boards_dictionary = self.file_manager.get_all_boards()
        board = boards_dictionary[self.main_ui.supported_boards.currentText()]
        port = self.device_manager.port

        self.commands = self.file_manager.compile_and_upload_commands(port, board)

        self.compile = True

    def display_save(self, already_called=False, save=None):
        """
        Loads the saved data onto the graphs on the GUI

        Args:
            save (str): the save file name
            already_called (bool): for some reason this function needs to be called twice
        """
        self.showing_data = True

        if not already_called:
            save, _ =  qtw.QFileDialog.getOpenFileName(
                self, "Open SideKick project", self.file_manager.save_manager.save_folder_path,
                "Save Files (*.txt)")

        if save:
            raw_data = self.file_manager.save_manager.get_saved_data(save)
        else:
            return

        self.message_handler.get_terminal(raw_data, live=False)
        self.top_graph.set_graph_data(raw_data)
        self.bottom_graph.set_graph_data(raw_data)

        self.update_terminal()
        self.top_graph.update_graph()
        self.bottom_graph.update_graph()

        if not already_called:
            time.sleep(0.1)
            self.display_save(True, save)

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

    def show_help(self):
        """
        Takes you to the help website
        TODO - help website
        """
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    def open_file(self):
        """
        Opens a file explorer window
        """
        file_path, _ =  qtw.QFileDialog.getOpenFileName(
            self, "Open SideKick project", self.file_manager.projects_path, "Arduino Files (*.ino)")

        if file_path:
            self.file_manager.set_current_project(file_path)

    def threaded_backend(self):
        """
        All backend tasks that need to be performed continually
        """

        ellipsis = threading.Thread(target=self.message_handler.update_ellipsis)
        ellipsis.start()

        while RUNNING:
            # Com ports
            port = self.device_manager.port
            self.avaliable_port_list = self.device_manager.scan_avaliable_ports(port, DEV)

            # Projects
            self.current_projects = self.file_manager.get_all_projects()

            # Saves
            self.current_saves = self.file_manager.get_all_saves()

            # If device manager has a connected device, show the data
            # otherwise the graphs shouldnt be overwritten
            if (self.device_manager.connected) or (not self.showing_data):

                if not self.showing_data:
                    raw_data = []
                if self.device_manager.connected:
                    raw_data = self.device_manager.raw_data
                    self.showing_data = False

                size = (self.main_ui.terminal.height(), self.main_ui.terminal.width())

                self.message_handler.get_terminal(raw_data, size)
                self.top_graph.set_graph_data(raw_data)
                self.bottom_graph.set_graph_data(raw_data)

            if self.record_light.blinking:
                data = self.device_manager.change_in_data
                self.file_manager.save_manager.save_data(data)
                self.device_manager.reset_difference(data)
            else:
                self.file_manager.save_manager.stop_save()

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

                error = self.device_manager.upload_script(self.commands[0], self.commands[1])

                self.message_handler.decode_debug_message(error)
                self.debug_window = True

                time.sleep(1)

                if port in self.avaliable_port_list:
                    self.connect_device(port)

                self.upload = False

if __name__ == "__main__":

    RUNNING = True

    app = qtw.QApplication(sys.argv)
    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)
    app.setAttribute(qtc.Qt.AA_Use96Dpi)

    main_gui = MainGUI()

    main_gui.show()
    app.exec_()

    main_gui.device_manager.terminate_device()
    main_gui.record_light.terminate_record()
    main_gui.message_handler.terminate_ellipsis()
    RUNNING = False

    project_selected = main_gui.file_manager.current_project
    board_selected = main_gui.main_ui.supported_boards.currentText()

    main_gui.file_manager.save_options(board_selected, project_selected)
