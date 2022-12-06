"""
Library manager
"""

import re
import subprocess

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from Ui.LibraryUi import Ui_MainWindow as library

class LibraryManager(qtw.QMainWindow):
    """
    updates and maintains the library manager window

    Args:
        qtw (QtWidgets): the main window functions
    """

    def __init__(self, file_manager, parent=None):
        super().__init__(parent=parent)

        # Attributes for the library manager
        self.library_ui = library()
        self.library_ui.setupUi(self)

        # Adds the scroll wheels
        self.library_ui.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.library_ui.scrollArea.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        # Defines the file_manager
        self.file_manager = file_manager

        # Adds place holder text
        self.library_ui.search.setPlaceholderText("Search for your library here.")

        # Loads the avaliable libraries
        regex = re.compile('[^a-zA-Z0-9 ./;_()#]')

        # Gets ALL libraries from the files
        self.installable = []
        with open(self.file_manager.arduino_lib_path,"r",encoding="utf8") as libraries:
            for line in libraries:
                if '"name":' in line:
                    self.installable.append(f"{regex.sub('', line).replace('name', '')}")
                elif '"sentence":' in line:
                    self.installable[-1] += f"\n{regex.sub('', line).replace('sentence', '')}"
                elif '"paragraph":' in line:
                    paragraph = regex.sub("", line).replace('paragraph', '').replace(". ", "\n")
                    self.installable[-1] += f"\n{paragraph}"

        # Checks which libraries are and aren't installed
        get_installed_libraries = f'"{self.file_manager.path}/Externals/arduino-cli.exe" lib list'
        with subprocess.Popen(
            get_installed_libraries, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True) as installed:

            installed_libraries  = installed.communicate()

        # Removes all installed libraries from the options
        for item in self.installable:
            if item in str(installed_libraries):
                self.installable.remove(item)

        # Connecting buttons
        self.library_ui.enter.clicked.connect(self.add_new_label)

    def add_new_label(self):
        """
        Adds more labels

        Args:
            name (_type_): _description_
        """

        # Clears all current text boxes
        for i in reversed(range(self.library_ui.scroll.layout().count())):
            self.library_ui.scroll.layout().itemAt(i).widget().setParent(None)

        # Removes exact copies
        search_results = []
        for item in self.installable:
            if self.library_ui.search.text().lower() in item.lower():
                search_results.append(item)

        # Removes ones with the same title
        search_results = list(dict.fromkeys(search_results))
        edited_search_results = []
        previous = [""]
        for item in search_results:
            header = item.split("\n")[0].replace(" ", "")
            if header not in previous:
                edited_search_results.append(item)
                previous.append(header)

        # Adds QtTextBrowsers to the QScrollArea
        check_boxes = []
        for item in edited_search_results:
            button = qtw.QCheckBox(self.library_ui.scroll)
            button.setMaximumWidth(500)
            button.setText(item)
            check_boxes.append(button)
            self.library_ui.scroll.layout().addWidget(check_boxes[-1])

        # Clears the search term
        self.library_ui.search.setText("")
