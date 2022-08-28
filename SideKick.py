from Graphing import Graphing
from Library import Library
from Backend import DataHandler
from FileManager import FileManager
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import webbrowser
import threading
import sys
import os

# Colours are defined here
colour_order = ["#FF0C0C", "#31f78e", "#02acf5","#fc7703","#9d03fc","#fce803","#fc03b1"]
accent_colour = "#252530"
text_colour = "#00f0c3"

# Definition to be appended to
supported_devices = {}

class EventHandler():

    # The Graphing window is ALWAYS the parent window
    # Launches the main graphing window, CSS is also used here
    def launchGraphing(self):
        app = qtw.QApplication(sys.argv)
        app.setStyleSheet(open("Ui/Style.css", "r").read())
        app_icon = qtg.QIcon("Ui/SideKick.ico")
        app.setWindowIcon(app_icon)
        self.graphing = Graphing()
        self.graphing.show()
        app.exec_()

    def launchLibrary(self):
        self.library = Library(self.graphing)
        self.library.show()

    # Sends the text from terminal to device
    def send_serial_input_to_device(self):
        if data.device != None:
            data.device.write(bytes(self.graphing.ui.lineEdit.text(), 'utf-8'))
        self.graphing.ui.lineEdit.setText("")

    # Changes the COM port beign used
    def update_com(self, value):
        self.disconnect_device()
        if value == "Select COM":
            return 0
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
        if self.graphing.ui.project_name.text() == "" or self.graphing.ui.project_name.text() == "Project Name":
            data.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>
                             <p><font color="#FF0C0C">Please enter a project name!</p>"""
            return 0
        if fileManager.add_new_project(self.graphing.ui.project_name.text()) == 0:
            data.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>
                             <p><font color="#FF0C0C">A project with that name already exists!</p>"""
            return 0
        data.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>"""

    # Compiles and Uploads current project
    def upload(self):
        # Disconnects everything and gets the project path.
        com = data.com_port
        self.disconnect_device()
        self.graphing.debug = True
        project_path = f'"C:/Users/{fileManager.user}/Documents/SideKick/SK Projects/{self.graphing.ui.project_paths.currentText()}/{self.graphing.ui.project_paths.currentText()}.ino"'

        # Creates upload on another thread and sets Html.
        upload = threading.Thread(target=data.upload, args=(com, project_path,))
        upload.start()
        self.graphing.ui.terminal.setHtml(f"""<h1><b><font color="#00f0c3">Uploading...</b></h1>""")

    # Stops and starts recordings.
    def record(self):
        data.save_data = not data.save_data
        if data.save_data:
            fileManager.start_new_save()

    def display_error(self):
        self.graphing.ui.terminal.setHtml(f"""<h1><b><font color="#00f0c3">Upload Failed</b></h1>{data.compile_output}""")
    # Loads up Orion Aerospace youtube channel
    def help(self):
        webbrowser.open("https://www.youtube.com/c/OrionAerospace", autoraise=True)

    # A spare function to test connectiions to buttons
    # NOT NECESSARY
    def test(self, value=""):
        print("This button works" + str(value))

if __name__ == "__main__":

    data = DataHandler()
    fileManager = FileManager()
    eventHandler = EventHandler()

    supported_devices = fileManager.get_all_boards()

    eventHandler.launchGraphing()
