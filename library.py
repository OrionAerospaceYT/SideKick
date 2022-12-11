"""
Library manager
"""

import re
import subprocess

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from Ui.LibraryUi import Ui_MainWindow as library

NUM_OF_CHARACTERS = 50

class LibraryManager(qtw.QMainWindow):
    """
    updates and maintains the library manager window

    Args:
        qtw (QtWidgets): the main window functions
    """

    def __init__(self, file_manager, parent=None):
        super().__init__(parent=parent)

        # Definition of attributes
        self.file_manager = file_manager
        self.check_boxes = []
        self.library_ui = library()

        self.library_ui.setupUi(self)

        # Adds the scroll wheels
        self.library_ui.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.library_ui.scrollArea.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        # Adds place holder text
        self.library_ui.search.setPlaceholderText("Search for your library here.")

        # Loads the avaliable libraries
        regex = re.compile('[^a-zA-Z0-9 ./;_()#]')

        # Gets ALL libraries from the files
        self.installable = []
        with open(self.file_manager.arduino_lib_path,"r",encoding="UTF-8") as libraries:
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
        self.library_ui.install.clicked.connect(self.install)

    def format_text(self, text):
        """
        formats the text such that the width is limited to a number of characters
        and all text is centered.

        Args:
            text (str): the text to process
        """

        text = text.replace('       ', ' ')
        text = text.replace("\n", "-")
        text = text.replace("u00c3", "<")
        text = text.replace("u003e", ">")
        text = text.replace("u003cbr/>", "")

        output_text = ""
        for index, string in enumerate(text.split("-")):
            if index == 0:
                output_text += f"{string}\n"
            else:
                temp_string =  f"{string} "
                if len(temp_string) > NUM_OF_CHARACTERS:
                    split_string = temp_string.split(" ")
                    index_counter = 0
                    final_string = [""]
                    for string_item in split_string:
                        if len(string_item) + len(final_string[index_counter]) < NUM_OF_CHARACTERS:
                            final_string[index_counter] += f"{string_item} "
                        else:
                            index_counter += 1
                            final_string.append(f"\n{string_item} ")
                    for string in final_string:
                        output_text += string
                    output_text += "\n"
                else:
                    output_text += f"{string} "
        return output_text

    def add_new_label(self):
        """
        Adds more labels

        Args:
            name (_type_): _description_
        """

        # Clears all current text boxes
        for i in reversed(range(self.library_ui.scroll.layout().count())):
            self.library_ui.scroll.layout().itemAt(i).widget().setParent(None)

        # Removes exact copiesarg
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
        self.check_boxes = []
        for item in edited_search_results:
            button = qtw.QCheckBox(self.library_ui.scroll)
            button.setText(self.format_text(item))
            self.check_boxes.append(button)
            self.library_ui.scroll.layout().addWidget(self.check_boxes[-1])

        # Clears the search term
        self.library_ui.search.setText("")

    def install(self):
        """
        Installs the libraries that the user has checked
        """
        # Iterates through every Check Box to check if it is checked
        for item in self.check_boxes:
            # Finds out if checked
            if item.isChecked():
                name = item.text().split("\n")[0]
                # Removes the first character if it is " "
                while name[0] == " ":
                    name = name[1:]
                # Installs the lib'rary
                with subprocess.Popen(f'"{self.file_manager.arduino_path}" lib install "{name}"'):
                    pass
