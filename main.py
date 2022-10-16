import threading
import sys
import webbrowser

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from graphing import Graphing
from Library import Library
from backend import DataHandler
from file_manager import FileManager

# Colours are defined here
COLOUR_ORDER = ["#FF0C0C",
                "#31f78e",
                "#02acf5",
                "#fc7703",
                "#9d03fc",
                "#fce803",
                "#fc03b1"]
ACCENT_COLOUR = "#252530"
TEXT_COLOUR = "#00f0c3"

# Definition to be appended to
supported_devices = {}


class EventHandler():
    """Deals with all events from the frontend"""

    def __init__(self):
        self.graphing = None
        self.library = None
        self.project_error = ""

    def launch_graphing(self):
        """
        The Graphing window is ALWAYS the parent window
        Launches the main graphing window, CSS is also used here
        """
        app = qtw.QApplication(sys.argv)
        app.setStyleSheet(open("Ui/Style.css", "r").read())
        app_icon = qtg.QIcon("Ui/SideKick.ico")
        app.setWindowIcon(app_icon)
        self.graphing = Graphing()
        self.graphing.show()
        app.exec_()

    def launch_library(self):
        """Launches the library manager window"""
        self.library = Library(self.graphing)
        self.library.show()

    def send_serial_input_to_device(self):
        """ Sends the text from terminal to device"""
        if data.device is not None:
            data.device.write(bytes(self.graphing.ui.lineEdit.text(), 'utf-8'))
        self.graphing.ui.lineEdit.setText("")

    def update_com(self, value):
        """Changes the COM port beign used"""
        self.disconnect_device()
        if value == "Select COM":
            return 0
        self.graphing.ui.COM.setText(value)
        data.device = None
        data.com_port = value
        data.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>"""
        self.graphing.ui.com_ports.setCurrentText("Select COM")
        self.graphing.debug = False

    def disconnect_device(self):
        """Discconects the SideKick device"""
        global data
        self.graphing.ui.COM.setText("")
        data.device = None
        data.com_port = None
        data = DataHandler()

    def new_project(self):
        """Creates a new project and handles the errors given"""
        if self.graphing.ui.project_name.text() == "":
            self.disconnect_device()
            self.project_error = """<font color="#ff003c">Please enter a project name!"""
            data.errors = 2
            return 0
        if fileManager.add_new_project(self.graphing.ui.project_name.text()) == 0:
            self.disconnect_device()
            self.project_error = """<font color="#ff003c">\
                                A project with that name already exists!"""
            data.errors = 2
            return 0

    def upload(self):
        """Compiles and Uploads current project"""
        com = data.com_port
        self.disconnect_device()
        data.debug = True

        project_path = f'"C:/Users/{fileManager.user}\
                        /Documents/SideKick/SK Projects/{self.graphing.ui.project_paths.currentText()}\
                        /{self.graphing.ui.project_paths.currentText()}.ino"'

        upload = threading.Thread(
            target=data.upload, args=(com, project_path,))
        upload.start()
        self.display_message("Uploading...")

    def record(self):
        """Stops and starts recordings."""
        data.save_data = not data.save_data
        if data.save_data:
            fileManager.start_new_save()

    def display_message(self, message=""):
        """"Displays error messages"""
        if data.errors == 1:
            message = f"""<h1><b><font color="#00f0c3">Upload Failed</b>\
                        </h1><p>{data.compile_output}</p>"""
        elif data.errors == 2:
            message = f"""<h1><b><font color="#00f0c3">Terminal</b></h1>\
                        <p>{self.project_error}</p>"""
        else:
            message = f"""<h1><b><font color="#00f0c3">{message}</b></h1>"""

        self.graphing.debug = True

        self.disconnect_device()

        self.graphing.ui.terminal.setHtml(message)

    def help(self):
        """Loads up Orion Aerospace youtube channel"""

        webbrowser.open(
            "https://www.youtube.com/c/OrionAerospace", autoraise=True)

    def test(self, value=""):
        """A spare function to test connectiions to buttons"""

        print("This button works" + str(value))


if __name__ == "__main__":

    data = DataHandler()
    fileManager = FileManager()
    event_handler = EventHandler()

    supported_devices = fileManager.get_all_boards()

    event_handler.launch_graphing()
