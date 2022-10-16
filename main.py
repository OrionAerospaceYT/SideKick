import webbrowser
import threading
import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from Backend import DataHandler
from FileManager import FileManager
from Graphing import Graphing
from Library import Library

# Colours are defined here
COLOUR_ORDER = ["#FF0C0C", "#31f78e", "#02acf5","#fc7703","#9d03fc","#fce803","#fc03b1"]
ACCENT_COLOUR = "#252530"
TEXT_COLOUR = "#00f0c3"

# Definition to be appended to
supported_devices = {}

"""Deals with events from the frontend"""
class EventHandler():

    def __init__(self):
        self.graphing = None
        self.library = None
        self.project_error = ""

    # The Graphing window is ALWAYS the parent window
    # Launches the main graphing window, CSS is also used here
    def launch_graphing(self):
        app = qtw.QApplication(sys.argv)
        with open("Ui/Style.css", "r") as style_file:
            app.setStyleSheet(style_file.read())
        app_icon = qtg.QIcon("Ui/SideKick.ico")
        app.setWindowIcon(app_icon)
        self.graphing = Graphing()
        self.graphing.show()
        app.exec_()

    # Launches the library manager window
    def launch_library(self):
        self.library = Library(self.graphing)
        self.library.show()

    def update_warning(self):
        # Creates a warning pop-up
        warning = qtw.QMessageBox()
        # Creats a warning icon
        warning.setIcon(qtw.QMessageBox.Warning)
        # Sets the text of the window
        warning.setText("Warning: ")
        warning.setInformativeText("""Library syntax may change with update\n\
                                    Current projects may not work with new code!""")
        warning.setWindowTitle("Update Warning")
        # Adds the OK button
        warning.setStandardButtons(qtw.QMessageBox.Ok)
        warning.buttonClicked.connect(self.test)
        warning.exec_()

    # Sends the text from terminal to device
    def send_serial_input_to_device(self):
        if data.device is not None:
            data.device.write(bytes(self.graphing.ui.lineEdit.text(), 'utf-8'))
        self.graphing.ui.lineEdit.setText("")

    # Changes the COM port beign used
    def update_com(self, value):
        self.disconnect_device()
        if value != "Select COM":
            self.graphing.ui.COM.setText(value)
            data.device = None
            data.com_port = value
            data.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>"""
            self.graphing.ui.com_ports.setCurrentText("Select COM")
            self.graphing.debug = False

    # Discconects the SideKick device
    def disconnect_device(self):
        self.graphing.ui.COM.setText("")
        data.device = None
        data.com_port = None
        data.__init__()

    # Creates a new project and handles the errors given
    def new_project(self):
        if self.graphing.ui.project_name.text() == "":
            self.disconnect_device()
            self.project_error = """<font color="#ff003c">Please enter a project name!"""
            data.errors = 2
        if file_manager.add_new_project(self.graphing.ui.project_name.text()) == 0:
            self.disconnect_device()
            self.project_error = """<font color="#ff003c">A project with that name already exists!"""
            data.errors = 2

    # Compiles and Uploads current project
    def upload(self):
        # Disconnects everything and gets the project path.
        com = data.com_port
        self.disconnect_device()
        data.debug = True

        project_path = f'"C:/Users/{file_manager.user}\
                        /Documents/SideKick/SK Projects/\
                        {self.graphing.ui.project_paths.currentText()}/\
                        {self.graphing.ui.project_paths.currentText()}.ino"'

        # Creates upload on another thread and sets Html.
        upload = threading.Thread(target=data.upload, args=(com, project_path,))
        upload.start()
        self.display_message("Uploading...")

    # Stops and starts recordings.
    def record(self):
        data.save_data = not data.save_data
        if data.save_data:
            file_manager.start_new_save()

    def display_message(self, message=""):

        if data.errors == 1:
            message = f"""<h1><b><font color="#00f0c3">
                      Upload Failed</b></h1><p>
                      {data.compile_output}</p>"""
        elif data.errors == 2:
            message = f"""<h1><b><font color="#00f0c3">
                      Terminal</b></h1><p>
                      {self.project_error}</p>"""
        else:
            message = f"""<h1><b><font color="#00f0c3">{message}</b></h1>"""

        self.graphing.debug = True

        self.disconnect_device()

        self.graphing.ui.terminal.setHtml(message)

    # Loads up Orion Aerospace youtube channel
    def help(self):
        webbrowser.open("https://www.youtube.com/c/OrionAerospace", autoraise=True)

    # A spare function to test connectiions to buttons
    # NOT NECESSARY
    def test(self, value=""):
        print("This button works" + str(value))

if __name__ == "__main__":

    data = DataHandler()
    file_manager = FileManager()
    event_handler = EventHandler()

    supported_devices = file_manager.get_all_boards()

    event_handler.launch_graphing()
