"""
Library manager
"""

import math

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from Ui.LibraryUi import Ui_MainWindow as library

class CheckBox:
    """
    Creates a checkbox which uses a text browser + html to create a
    good looking way of displaying all relevant information of a
    library:
    """

    def __init__(self, name, html, versions, parent=None):

        self.name = name

        self.vertical_layout = qtw.QVBoxLayout()

        self.versions = qtw.QComboBox()
        for item in reversed(versions):
            self.versions.addItem(item)

        self.install = qtw.QPushButton("Install")

        if parent:
            self.install.clicked.connect(lambda: parent.install(self.get_version(),
                                                                self.name))
        self.vertical_layout.addWidget(self.install)
        self.vertical_layout.addWidget(self.versions)

        self.horizontal_layout = qtw.QHBoxLayout()

        self.info = qtw.QTextBrowser()
        self.info.setHtml(html)
        self.info.setOpenExternalLinks(True)
        self.info.setMinimumHeight(self.calculate_num_lines(html, self.info.size().width()))

        self.horizontal_layout.addLayout(self.vertical_layout)
        self.horizontal_layout.addWidget(self.info)

    def calculate_num_lines(self, html, width):
        """
        test

        Args:
            html (_type_): _description_

        Returns:
            _type_: _description_
        """
        doc = qtg.QTextDocument()
        doc.setHtml(html)
        num_blocks = 0
        block = doc.begin()
        i = 0
        while block.isValid():
            block_width = block.layout().boundingRect().width()
            if block_width > width:
                if i == 0:
                    num_blocks += math.ceil(block_width / width) * 40
                else:
                    num_blocks += math.ceil(block_width / width) * 30
            else:
                num_blocks += 1
            block = block.next()
            i += 1
        return num_blocks * 40

    def get_version(self):
        """
        returns the version that is currently selected
        """
        return str(self.versions.currentText())

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
        self.parent = parent
        self.library_ui = library()
        self.file_manager = file_manager
        self.check_boxes = []

        self.library_ui.setupUi(self)

        # Adds place holder text
        self.library_ui.search.setPlaceholderText("Search for your library here.")

        # Connecting buttons
        self.library_ui.enter.clicked.connect(self.update_labels)
        self.library_ui.search.returnPressed.connect(self.update_labels)
        self.library_ui.search.returnPressed.connect(self.update_labels)

        self.show()

    def clear_layout(self, layout):
        """
        Removes all layouts and widgets from the screen.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def update_labels(self):
        """
        Updates the libraries that are on display.
        """
        self.clear_layout(self.library_ui.libraries)

        for name in self.file_manager.get_all_libraries(self.library_ui.search.text()):
            versions = self.file_manager.get_versions(name)
            check_box = CheckBox(name, self.file_manager.get_html(name), versions, parent=self)
            self.check_boxes.append(check_box.horizontal_layout)
            self.library_ui.libraries.addLayout(self.check_boxes[-1])

    def install(self, version, name):
        """
        calls the actuall install function on a thread

        Args:
            version (string): the selected version to install
            name (string): the name of the library to install   
        """

        self.parent.cli_manager.communicate(f"lib install \"{name}@{version}\"")
