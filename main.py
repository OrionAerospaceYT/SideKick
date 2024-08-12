"""
This is the main python file responsible for having
the debugging window open.

#TODO -> Fix the terminal HTML being slow
#TODO -> Add warnings for uploading without a device being selected
"""

import os
import sys
import threading
import time
import webbrowser

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from actuator import ActuatorGUI
from boards import BoardsManager
from library import LibraryManager
from device_manager import DeviceManager
from file_manager import FileManager
from cli_manager import CliManager
from terminal_manager import Terminal

from widgets import Graph
from widgets import RecordLight
from widgets import SideMenu
from widgets import SideKickLite

from message_handler import MessageHandler
from Ui.GraphingUi import Ui_MainWindow as main_window

DEV = False
CONSCIOS_PATH = ""

class MainGUI(qtw.QMainWindow):
    """
    Launches the main window (debugging window)

    This class inherits QMainWindow from PyQt6.QtWidgets as
    it holds the gui object which we need to modify.

    This class also usues the Graph class from graphs.py

    Args:
        qtw (QtWidgets): the main window functions
    """

    def __init__(self):

        super().__init__()

        self.main_ui = main_window()
        self.main_ui.setupUi(self)

        self.main_ui.debugger.setVisible(False)

        self.set_screen_size()

        # Associative classes are initialised here
        self.actuator = None
        self.device_manager = DeviceManager(self)

        self.file_manager = FileManager(DEV, CONSCIOS_PATH)

        board, project, lite = self.file_manager.load_options()
        self.sk_lite = SideKickLite(self.main_ui.sk_lite, lite)

        self.cli_manager = CliManager(self.file_manager.paths["arduino"])

        self.top_graph = Graph(key="1")
        self.bottom_graph = Graph(key="2")
        self.message_handler = MessageHandler(self.main_ui.debugger,
                                              self.main_ui.debug_log,
                                              self.main_ui.home_screen,
                                              self.main_ui.message)
        self.record_light = RecordLight()
        self.side_menu = SideMenu(
            self.main_ui.settings,
            self.main_ui.device_settings,
            self.main_ui.side_menu)

        self.terminal = Terminal(self.main_ui.terminal)

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
        self.main_ui.message.setPlaceholderText("Enter device message here.")
        self.main_ui.bottom_update.setAlignment(
            qtc.Qt.AlignmentFlag.AlignRight | qtc.Qt.AlignmentFlag.AlignVCenter)

        # Attributes for event handling are defined here
        self.running = True
        self.showing_data = False
        self.upload = False

        self.avaliable_port_list = []
        self.current_saves = []

        threaded_blinking_record = threading.Thread(
            target=self.record_light.threaded_blink, args=(),)
        threaded_blinking_record.start()

        threaded_backend_loop = threading.Thread(
            target=self.threaded_backend, args=(),)
        threaded_backend_loop.start()

        self.main_ui.supported_boards.setCurrentText(board)

        self.file_manager.current_project = project

        self.device_manager.auto_connect = True

        self.displayed_save = None
        self.export_error = False

        self.display_size()

        self.file_manager.set_all_boards(self.cli_manager)
        self.reset_supported_boards()

        timer = qtc.QTimer(self)
        timer.setInterval(0)
        timer.timeout.connect(self.update)
        timer.start()

    def set_screen_size(self):
        """
        On opening, set the screen size to a good dimensions relative to the monitor.
        """
        desktop = qtg.QGuiApplication.primaryScreen().availableGeometry()
        height = int(desktop.height() * 0.75)
        width = min(int(height * 1.618), int(desktop.width() * 0.75))

        self.resize(width, height)

    def open_library_manager(self):
        """
        Opens the library manager window
        """
        LibraryManager(self.file_manager, self)

    def open_boards_manager(self):
        """
        Opens the board manager window
        """
        BoardsManager(self.file_manager, self.cli_manager, self)

    def open_actuator_gui(self):
        """
        Opens the actuator tuning suite
        """
        if self.actuator is not None:
            return

        self.actuator = ActuatorGUI(self.device_manager, self)
        self.actuator.setAttribute(qtc.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.actuator.show()
        self.display_size()
        self.actuator.destroyed.connect(self.close_actuator_gui)

    def close_actuator_gui(self):
        """
        Sets actuator_gui to false
        """
        self.actuator = None

    def reset_supported_boards(self):
        """
        Resets all of the shown widgets on the boards drop down menu.
        """
        boards = self.file_manager.board_names

        while self.main_ui.supported_boards.currentText():
            self.main_ui.supported_boards.removeItem(0)

        for board in boards:
            self.main_ui.supported_boards.addItem(board[0])

    def connect_buttons(self):
        """
        Connects the buttons/drop-downs on the gui to python functions
        """

        self.main_ui.record.clicked.connect(self.record_light.update_recording)
        self.main_ui.file.clicked.connect(self.open_file_manager)
        self.main_ui.device.clicked.connect(self.open_device_manager)
        self.main_ui.upload.clicked.connect(self.upload_project)
        self.main_ui.quit.clicked.connect(self.message_handler.close_debug_window)
        self.main_ui.compile.clicked.connect(self.compile_project)
        self.main_ui.disconnect.clicked.connect(self.device_manager.terminate_device)
        self.main_ui.library_manager.clicked.connect(self.open_library_manager)
        self.main_ui.boards_manager.clicked.connect(self.open_boards_manager)
        self.main_ui.show_save.clicked.connect(self.display_save)
        self.main_ui.message.returnPressed.connect(self.send)
        self.main_ui.select_project.clicked.connect(self.open_file)
        self.main_ui.new_project.clicked.connect(self.new_project)
        self.main_ui.help.clicked.connect(self.show_help)
        self.main_ui.com_ports.currentIndexChanged.connect(self.connect_device)
        self.main_ui.tune_actuators.clicked.connect(self.open_actuator_gui)
        self.main_ui.arduino_cli.clicked.connect(self.display_cli)
        self.main_ui.full_screen.clicked.connect(
            lambda: self.message_handler.expand_debug(self.main_ui.full_screen))
        self.main_ui.export_save.clicked.connect(self.export_save)

    def connect_keyboard_shortcuts(self):
        """
        Connects keyboard shortcuts to their respective functions:
            ctrl + x (disconnect)
            ctrl + s (verify/compile)
            ctrl + u (upload)
            ctrl + r (record)
            ctrl + h (help)
        """

        disconnect = qtg.QShortcut(qtg.QKeySequence("ctrl+x"), self)
        disconnect.activated.connect(self.device_manager.terminate_device)

        compile_code = qtg.QShortcut(qtg.QKeySequence("ctrl+s"), self)
        compile_code.activated.connect(self.compile_project)

        upload = qtg.QShortcut(qtg.QKeySequence("ctrl+u"), self)
        upload.activated.connect(self.upload_project)

        record = qtg.QShortcut(qtg.QKeySequence("ctrl+r"), self)
        record.activated.connect(self.record_light.update_recording)

        help_website = qtg.QShortcut(qtg.QKeySequence("ctrl+h"), self)
        help_website.activated.connect(self.demo_function)

        tune_actuators = qtg.QShortcut(qtg.QKeySequence("ctrl+a"), self)
        tune_actuators.activated.connect(self.open_actuator_gui)

        full_screen = qtg.QShortcut(qtg.QKeySequence("ctrl+q"), self)
        full_screen.activated.connect(
            lambda: self.message_handler.expand_debug(self.main_ui.full_screen))

        zoom_in = qtg.QShortcut(qtg.QKeySequence("ctrl+="), self)
        zoom_in.activated.connect(self.increase_font_size)

        zoom_out = qtg.QShortcut(qtg.QKeySequence("ctrl+-"), self)
        zoom_out.activated.connect(self.decrease_font_size)

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

        if self.cli_manager.running:
            self.main_ui.top_update.setStyleSheet("QLabel{font-size:14pt}")
            self.main_ui.top_update.setText(
                self.message_handler.get_status("Running"))
        elif self.device_manager.error is not None and self.device_manager.device is None:
            self.main_ui.top_update.setText("Error, could not connect!")
        elif self.export_error:
            self.main_ui.top_update.setText("Please show save first!")
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

    def update(self):
        """
        calls all update functions
        """

        # update the boards
        if self.file_manager.update:
            self.reset_supported_boards()
            self.file_manager.update = False

            board = self.file_manager.load_options()[0]
            self.main_ui.supported_boards.setCurrentText(board)

        # debug
        output, cmd_type = self.cli_manager.get_output()
        if output is not None:
            self.message_handler.decode_debug_message(output, cmd_type)
            if self.upload and not self.cli_manager.get_status():
                if self.actuator is not None:
                    self.actuator.done_upload()
                self.connect_device(self.device_manager.last_port)
                self.upload = False

        # set labels
        name = self.file_manager.parsed_project_name()
        if name:
            if len(name) > 21:
                name = name[0:18] + "..."
            self.main_ui.selected_project.setText(name)
        else:
            self.main_ui.selected_project.setText("Select A Project!")

        # update functions
        self.update_ports()
        self.top_graph.update_graph()
        self.bottom_graph.update_graph()

        # record light
        self.turn_on_rec_light(self.record_light.show)

        self.update_compile_and_upload()

        # terminal data
        self.terminal.update_text()

        # device messages
        if self.device_manager.connected:
            self.main_ui.bottom_update.setText("Connected")
            self.main_ui.com_ports.setCurrentText(self.device_manager.port)
        else:
            self.main_ui.bottom_update.setText("Not Connected")

    def new_project(self):
        """
        Gets the directory URL from getExistingDirectoryUrl with a
        QFileDialog and then creates a sidekick project in that directory.
        """
        folder_path = qtw.QFileDialog.getSaveFileName(self,
                            'Create Folder', self.file_manager.paths["projects"], 'Folders (*)')[0]

        if folder_path:
            self.file_manager.add_new_project(folder_path)

    def connect_device(self, port):
        """
        Connects new devices through device manager and updates com por[t in
        self.message_handler

        Args:
            port (string): the com port selected in the gui
        """
        self.clear_all_data()

        baud = self.main_ui.baud_rate.itemText(0)

        if self.device_manager.port == port:
            self.device_manager.terminate_device()
            return

        if self.device_manager.port is not None:
            self.device_manager.terminate_device()

        if DEV and port == "emulate":
            self.device_manager.connect_device(port, baud, dev=True)
        else:
            self.device_manager.connect_device(port, baud)

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

    def search(self, element:str, list_of_lists:list) -> str:
        """
        Goes through a list of lists which returns the second element
        in the sub list given the first.

        Args:
            element (str): the element key
            list_of_lists (list): second element in sub list

        Returns:
            str: the second element in the sub list
        """
        for sublist in list_of_lists:
            if sublist[0] == element:
                return sublist[1]
        return None

    def upload_project(self, actuator=False):
        """
        Gets selected board to upload to
        Checks if a device is connected to the gui
        Disconnects the device to upload
        Compiles the script and then uploads the script
        """
        if self.upload:
            return

        temp = self.file_manager.current_project

        if actuator:
            self.file_manager.current_project = self.file_manager.paths["actuator"]
        elif DEV:
            self.file_manager.set_dev_file()

        board = self.search(self.main_ui.supported_boards.currentText(),
                            self.file_manager.board_names)
        port = self.device_manager.port

        self.upload = True

        self.cli_manager.communicate(
            f"compile --fqbn {board} \"{self.file_manager.current_project}\"",
            "upload")

        self.device_manager.terminate_device()

        self.cli_manager.communicate(
            f"upload -p {port} --fqbn {board} \"{self.file_manager.current_project}\"",
            "upload")

        self.file_manager.current_project = temp

    def compile_project(self):
        """
        Compiles the script
        """
        temp = self.file_manager.current_project

        if DEV:
            self.file_manager.set_dev_file()

        board = self.search(self.main_ui.supported_boards.currentText(),
                            self.file_manager.board_names)

        self.cli_manager.communicate(
            f"compile --fqbn {board} \"{self.file_manager.current_project}\"",
            "compile")

        self.file_manager.current_project = temp

    def display_save(self, save=None):
        """
        Loads the saved data onto the graphs on the GUI

        Args:
            save (str): the save file name
        """

        # Disconnect all devices and set the GUI to the showing save mode
        self.showing_data = True
        self.device_manager.terminate_device()
        self.clear_all_data()

        # Load the save's data into a variable and check there is data
        save, _ =  qtw.QFileDialog.getOpenFileName(
            self, "Open SideKick project",
            self.file_manager.save_manager.save_folder_path,
            "Save Files (*.sk)")

        if not save:
            return

        self.displayed_save = save
        raw_data = self.file_manager.save_manager.get_saved_data(save)

        # Set the data for the graph and the HTML for the terminal
        self.message_handler.get_save_html(raw_data)
        self.top_graph.set_graph_data(raw_data)
        self.bottom_graph.set_graph_data(raw_data)

        # Display the save's data to the user on the screen
        self.top_graph.update_graph()
        self.bottom_graph.update_graph()
        self.main_ui.terminal.setHtml(self.message_handler.terminal_html)

    def demo_function(self):
        """
        Prints "Hello world!"
        Used to demo connected buttons
        """
        print("Hello world!")

    def show_help(self):
        """
        Takes you to the help website
        """
        webbrowser.open("https://github.com/OrionAerospaceYT/SideKick/blob/main/README.md")

    def open_file(self):
        """
        Opens a file explorer window
        """
        path = ""
        for item in self.file_manager.current_project.split("/")[:-2]:
            path += item + self.file_manager.sep

        file_path, _ =  qtw.QFileDialog.getOpenFileName(
            self, "Open SideKick project",
            path,
            "Arduino Files (*.ino)")

        if file_path:
            self.file_manager.set_current_project(file_path)

    def send(self):
        """
        A function to check wether or not the message entered is for the CLI or for the
        device manager.
        """
        if self.message_handler.minimized:
            self.device_manager.send(self.main_ui.message.text())
        else:
            self.cli_manager.communicate(self.main_ui.message.text(), "usr")
        self.main_ui.message.setText("")

    def display_cli(self):
        """
        Shows the debug log in full screen so that the user can enter cli commands.
        """
        self.message_handler.set_debug_html()
        self.message_handler.expand_debug(self.main_ui.full_screen)

    def clear_all_data(self):
        """
        A wrapper function that clears the graphs and terminal.
        """
        self.top_graph.clear_graph()
        self.bottom_graph.clear_graph()

        self.message_handler.clear_terminal()
        self.terminal.clear()

    def export_save(self):
        """
        Export the currently displayed save.
        """
        if self.showing_data:
            folder_path = qtw.QFileDialog.getSaveFileName(self,
                            'Create Folder',
                            self.file_manager.save_manager.save_folder_path,
                            'Save Files (*.csv)')[0]
            if folder_path:
                self.file_manager.save_manager.export_save(self.displayed_save, folder_path)
            self.export_error = False
        else:
            self.export_error = True

    def increase_font_size(self):
        """
        Increases the font sizes by 10% if the user wants.
        """
        self.file_manager.change_size_stylesheet(increase=True)
        self.display_size()

    def decrease_font_size(self):
        """
        Decreases the font sizes by 10% if the user wants.
        """
        self.file_manager.change_size_stylesheet(increase=False)
        self.display_size()

    def display_size(self):
        """
        Display the new size to the screen.
        """
        stylesheet, scale = self.file_manager.get_size_stylesheet()
        self.setStyleSheet(stylesheet)
        self.main_ui.side_menu.setMinimumWidth(int(300*scale))
        combo_box_width = 120 - int(20/scale)
        if scale > 0.8:
            combo_box_width = 100+int(20*scale**2.4)

        self.main_ui.com_ports.setFixedWidth(combo_box_width)
        if self.actuator is not None:
            self.actuator.actuators_ui.type.setFixedWidth(combo_box_width-20)

    def threaded_backend(self):
        """
        All backend tasks that need to be performed continually
        
        
        PLAN:
        
        CLI States : running user command, compile, upload
        Record States : on, off
        Displaying save states : on, off
        Auto Connect states : on, off
        """

        ellipsis = threading.Thread(target=self.message_handler.update_ellipsis)
        ellipsis.start()

        cli = threading.Thread(target=self.cli_manager.threaded_call, args=(),)
        cli.start()

        while self.running:
            # Com ports
            self.avaliable_port_list = self.device_manager.scan_avaliable_ports(DEV)

            # Saves
            self.current_saves = self.file_manager.get_all_saves()

            # If device manager has a connected device, show the data
            # otherwise the graphs shouldnt be overwritten
            if (self.device_manager.connected) or (not self.showing_data):

                if not self.showing_data:
                    raw_data = []
                if self.device_manager.connected:
                    raw_data = self.device_manager.raw_data
                    self.device_manager.raw_data = self.device_manager.raw_data[len(raw_data):]
                    self.showing_data = False

                if self.device_manager.start_rec:
                    self.device_manager.start_rec = False
                    self.record_light.start_recording()
                elif self.device_manager.end_rec:
                    self.device_manager.end_rec = False
                    self.record_light.end_recording()

                # Updating display data
                self.top_graph.set_graph_data(raw_data)
                self.bottom_graph.set_graph_data(raw_data)
                self.terminal.append_data(raw_data)

            # Recording functionality
            if self.record_light.blinking:
                for i, data in enumerate(raw_data):
                    data = data.replace("&amp;", "&")
                    data = data.replace("&lt;", "<")
                    data = data.replace("&quot;", "\"")
                    data = data.replace("&#39;", "'")
                    raw_data[i] = data.replace("&gt;", ">")
                self.file_manager.save_manager.save_data(raw_data)
            else:
                self.file_manager.save_manager.stop_save()

    def close_gui(self):
        """
        Safely closes down the GUI.
        """
        self.running = False
        # waits for whole backend call to finish before ending all of the other threads
        # prevents errors
        time.sleep(1)

        self.device_manager.terminate_device()
        self.record_light.terminate_record()
        self.message_handler.terminate_ellipsis()
        self.cli_manager.terminate()

if __name__ == "__main__":

    if "-d" in sys.argv:
        DEV = True

        if os.path.exists(sys.argv[2]):
            CONSCIOS_PATH = sys.argv[2]
        else:
            print(f"<<< ERROR >>> Please enter a valid file path! {sys.argv[2]}")
            sys.exit()

    app = qtw.QApplication(sys.argv)
    app_icon = qtg.QIcon("Ui/SideKick.ico")
    app.setWindowIcon(app_icon)

    main_gui = MainGUI()

    main_gui.show()
    app.exec()

    main_gui.close_gui()

    project_selected = main_gui.file_manager.current_project
    board_selected = main_gui.main_ui.supported_boards.currentText()
    sk_lite = main_gui.sk_lite.state

    main_gui.file_manager.save_options(board_selected, project_selected, sk_lite)
