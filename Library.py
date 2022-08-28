from Ui.LibraryUi import Ui_MainWindow as library
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5 import QtWidgets as qtw
import subprocess
import os
import re
import __main__

class Library(qtw.QMainWindow):

    def __init__(self, parent = None):
        super(Library, self).__init__(parent=parent)

        # Defines the library window
        self.ui = library()
        self.ui.setupUi(self)

        # Adds the scroll wheels
        self.ui.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.ui.scrollArea.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)

        # Adds place holder text
        self.ui.search.setPlaceholderText("Search for your library here.")

        # Loads the avaliable libraries
        libraries_file = f"C:/Users/{__main__.fileManager.user}/AppData/Local/Arduino15/library_index.json"
        regex = re.compile('[^a-zA-Z0-9 ./;_()#]')

        # Gets ALL libraries from the files
        self.installable = []
        with open(libraries_file,"r",encoding="utf8") as libraries:
            for line in libraries:
                if '"name":' in line:
                    self.installable.append(f"""{regex.sub("", line).replace('name', '')}""")
                elif '"sentence":' in line:
                    self.installable[-1] += f"""\n{regex.sub("", line).replace('sentence', '')}"""
                elif '"paragraph":' in line:
                    paragraph = regex.sub("", line).replace('paragraph', '').replace(". ", "\n       ")
                    self.installable[-1] += f"""\n{paragraph}"""

        # Checks which libraries are and aren't installed
        cwd = os.getcwd()
        get_installed_libraries = f'"{cwd}/Externals/arduino-cli.exe" lib list'
        installed = subprocess.Popen(get_installed_libraries, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        installed_libraries, error = installed.communicate()

        # Removes all installed libraries from the options
        for item in self.installable:
            if item in str(installed_libraries):
                self.installable.remove(item)

        # Connects buttons
        self.ui.enter.clicked.connect(self.add_new_label)
        self.ui.install.clicked.connect(self.install)

    def install(self, arg):
        # Iterates through every Check Box to check if it is checked
        for item in self.checkBoxes:
            # Finds out if checked
            if item.isChecked():
                cwd = os.getcwd()
                name = item.text().split("\n")[0]
                # Removes the first character if it is " "
                while name[0] == " ":
                    name = name[1:]
                # Installs the library
                installing = subprocess.Popen(f""""{cwd}/Externals/arduino-cli.exe" lib install "{name}" """)
                installed, error = installing.communicate()

    def add_new_label(self, name):
        # Clears all current text boxes
        for i in reversed(range(self.ui.scroll.layout().count())):
            self.ui.scroll.layout().itemAt(i).widget().setParent(None)

        # Removes exact copies
        search_results = []
        for item in self.installable:
            if self.ui.search.text().lower() in item.lower():
                search_results.append(item)

        # Removes ones with the same title
        search_results = list(dict.fromkeys(search_results))
        previous = [""]
        for item in search_results:
            header = item.split("\n")[0].replace(" ", "")
            if header in previous:
                search_results.remove(item)
            else:
                previous.append(header)

        # Adds QtTextBrowsers to the QScrollArea
        self.checkBoxes = []
        for item in search_results:
            button = qtw.QCheckBox(self.ui.scroll)
            button.setText(item)
            self.checkBoxes.append(button)
            self.ui.scroll.layout().addWidget(self.checkBoxes[-1])

        # Clears the search term
        self.ui.search.setText("")
