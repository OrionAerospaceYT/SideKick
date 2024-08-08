"""
Controls the gui which allows the user to install other boards    
"""

import threading

from PyQt5 import QtWidgets as qtw

from Ui.BoardsUi import Ui_MainWindow as boards

from widgets import BoardWidget

from globals import SELECTED_WIDGET_QSS, NORMAL_WIDGET_QSS

class BoardsManager(qtw.QMainWindow):
    """
    updates and maintains the library manager window
    inherits qtw.QMainWindow so it inherits the properties needed
    for the gui

    Attributes:
        file_manager (FileManager): the file manager from MainGUI
        check_boxes (list): the checkboxes that are on display
        boards_ui (TODO): the library GUI
        installable (list): the list of installable libraries
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.boards_ui = boards()
        self.boards_ui.setupUi(self)

        # Definition of attributes
        self.parent = parent
        self.file_manager = self.parent.file_manager
        self.cli_manager = self.parent.cli_manager
        self.widgets = []


        self.selected = -1

        # Connecting buttons
        self.boards_ui.install.clicked.connect(self.install)

        self.update_labels()

        self.resize(int(self.parent.width()*0.8), int(self.parent.height()*0.8))

        self.setWindowModality(2)

        self.show()

    def update_labels(self):
        """
        Updates the libraries that are on display.
        """
        for name in list(self.file_manager.boards.keys()):
            versions = self.file_manager.get_versions(name, self.file_manager.boards)
            html = self.file_manager.get_html(name, self.file_manager.boards)
            self.widgets.append(BoardWidget(name, versions, html, len(self.widgets), self))
            self.boards_ui.boards.addWidget(self.widgets[-1])

    def update_selected(self, index):
        """
        Testing parent function calls
        """
        while self.boards_ui.versions.currentText():
            self.boards_ui.versions.removeItem(0)

        self.boards_ui.install.setText("Select a board to install")

        if index == self.selected:
            self.selected = -1
        else:
            self.selected = index

        for indx, widget in enumerate(self.widgets):
            widget.setStyleSheet(NORMAL_WIDGET_QSS)
            if indx == self.selected:
                widget.setStyleSheet(SELECTED_WIDGET_QSS)
                self.boards_ui.install.setText("Install: " + widget.name)
                for item in widget.versions:
                    self.boards_ui.versions.addItem(item)

        if not self.boards_ui.versions.currentText():
            self.boards_ui.versions.addItem("N/A")

    def install(self):
        """
        Calls the actuall install function on a thread.
        """
        if self.selected == -1:
            return

        name = self.widgets[self.selected].name
        version = self.boards_ui.versions.currentText()

        architecture = self.file_manager.boards[name]["architecture"]
        self.parent.cli_manager.communicate(
            f"core install \"{architecture}@{version}\"")

        threaded_wait = threading.Thread(
            target=self.wait_to_update_boards,
            args=(f"core install \"{architecture}@{version}\"",),)
        threaded_wait.start()

    def wait_to_update_boards(self, cmd):
        """
        Waits for the install command to be run before
        TODO
        """
        while (cmd in self.cli_manager.commands.keys()) or self.cli_manager.running:
            pass
        self.file_manager.set_all_boards(self.cli_manager)
