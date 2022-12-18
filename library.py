"""
Library manager
"""

import re
import subprocess

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from Ui.LibraryUi import Ui_MainWindow as library

NUM_OF_CHARACTERS = 80
EXCLUDED_CHARACTERS = [("\n", "-"),
                       ("       ", " "),
                       ("u003c", "<"),
                       ("u003e", ">")]

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
        self.setFixedSize(750, 500)

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
        self.library_ui.search.returnPressed.connect(self.add_new_label)

    def format_text(self, text):
        """
        gets the text and splits it into the sections then re assembles it
        so that it does not exceed theline length

        Args:
            text (str): the string to be formatted

        Returns:
            str: the formatted string
        """

        output_text = ""
        header_displayed = False
        display = False

        # iterates through each "\n" which is represented by the "-"
        for string in text.split("-"):

            # the first line is slightly different
            # the indent is key and checks must be made that it
            # is a title not an empty line
            if not header_displayed:
                for char in string:
                    if char.isalnum():
                        display = True
                        break
                if display:
                    output_text += f"   <h2><font color='#00f0c3'>{string}</font></h2><br>   "
                    name = string
                    output_text += "<font color='#FFFFFF' size='+2'>"
                    header_displayed = True
                continue

            temp_string =  f"{string} "

            # if the line it too long, split it up and parse it together over multiple lines
            if len(temp_string) > NUM_OF_CHARACTERS:
                split_string = temp_string.split(" ")
                index_counter = 0
                final_string = [""]

                # goes through each item keeping track of how long the line is
                for string_item in split_string:
                    if len(string_item) + len(final_string[index_counter]) < NUM_OF_CHARACTERS:
                        final_string[index_counter] += f"{string_item} "
                    else:
                        index_counter += 1
                        final_string.append(f"<br>    {string_item} ")

                for string in final_string:
                    output_text += string
                output_text += "<br>    "
            else:
                output_text += f"{string}<br>    "

        return output_text, name

    def get_formatted_text(self, text):
        """
        removes all html and other tags with regex
        then formats the text using self.format_text()
        and finally adds the new characters

        Args:
            text (str): the text to process

        Returns:
            str: the formatted string
        """

        for excluded_string in EXCLUDED_CHARACTERS:
            text = text.replace(excluded_string[0], excluded_string[1])

        # formats the text in terms of line length
        output_text, name = self.format_text(text)

        # removes any unwanted spaces and adds new lines before and after
        output_text = output_text.replace("<br>     ", "<br>    ")
        output_text = f"<br>{output_text}<br>"

        return output_text, name

    def text_to_qicon(self, text):
        """
        Converts the input text to a QIcon object.

        Args:
            text (string): the html that needs to be converted to a QIcon

        Returns:
            QIcon: the html
        """

        # creates a QTextDocument from the html
        document = qtg.QTextDocument()
        document.setDocumentMargin(0)

        formatted_text, name = self.get_formatted_text(text)
        document.setHtml(formatted_text)

        # converts the QTextDocument to a QIcon so that it can then be
        # set to the button icon
        pixmap = qtg.QPixmap(document.size().toSize())
        pixmap.fill(qtc.Qt.transparent)
        painter = qtg.QPainter(pixmap)
        document.drawContents(painter)
        painter.end()

        return qtg.QIcon(pixmap), name, pixmap.size()

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
        self.check_boxes = []
        for item in edited_search_results:

            button = qtw.QCheckBox(self.library_ui.scroll)

            icon, name, size = self.text_to_qicon(item)

            button.setIcon(icon)
            button.setIconSize(size)

            # for the installation the name is set to the button text
            # but the colour is the same as the background so that the
            # name cannot be seen
            button.setText(name)
            button.setStyleSheet("""color:#32323C""")

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
                name = item.text()
                # Removes the first character if it is " "
                print(name)
                while name[0] == " ":
                    name = name[1:]
                # Installs the lib'rary
                with subprocess.Popen(f'"{self.file_manager.arduino_path}" lib install "{name}"'):
                    pass
