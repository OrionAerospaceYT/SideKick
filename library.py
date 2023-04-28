"""
Library manager
"""

import re
import subprocess
import threading

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from Ui.LibraryUi import Ui_MainWindow as library

class CheckBox:
    """
    Creates a checkbox which uses a text browser + html to create a
    good looking way of displaying all relevant information of a
    library:
    """
    def __init__(self, html):
        self.horizontal_layout = qtw.QHBoxLayout()

        self.info = qtw.QTextBrowser()
        self.info.setHtml(html)
        self.info.setOpenExternalLinks(True)

        self.checkbox = qtw.QCheckBox()

        self.horizontal_layout.addWidget(self.checkbox)
        self.horizontal_layout.addWidget(self.info)


class LibraryManager(qtw.QMainWindow):
    """
    updates and maintains the library manager window
    inherits qtw.QMainWindow so it inherits the properties needed
    for the gui

    Attributes:
        file_manager (FileManager): the file manager from MainGUI
        check_boxes (list): the checkboxes that are on display
        library_ui (library): the library GUI
        installable (list): the list of installable libraries
    """

    def __init__(self, file_manager, parent=None):
        super().__init__(parent=parent)

        # Definition of attributes
        self.library_ui = library()
        self.file_manager = file_manager
        self.check_boxes = []

        self.library_ui.setupUi(self)

        # Adds the scroll wheels
        self.setFixedSize(750, 500)

        # Adds place holder text
        self.library_ui.search.setPlaceholderText("Search for your library here.")

        # Connecting buttons
        self.library_ui.enter.clicked.connect(self.add_new_label)
        self.library_ui.search.returnPressed.connect(self.add_new_label)
        self.library_ui.install.clicked.connect(self.install)
        self.library_ui.search.returnPressed.connect(self.add_new_label)
        print(self.file_manager.get_all_libraries("ser"))

        self.show()

    def add_new_label(self):
        """
        Adds more labels

        Args:
            name (_type_): _description_
        """
        for item in self.file_manager.get_all_libraries(self.library_ui.search.text()):
            check_box = CheckBox(self.file_manager.get_html(item))
            self.check_boxes.append(check_box.horizontal_layout)
            self.library_ui.libraries.addLayout(self.check_boxes[-1])

    def install(self):
        """
        calls the actuall install function on a thread
        """

        install = threading.Thread(target=self.threaded_install)
        install.start()

    def threaded_install(self):
        """
        Installs the libraries that the user has checked
        """
        pass
