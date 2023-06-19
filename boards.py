"""
Controls the gui which allows the user to install other boards    
"""
from PyQt5 import QtWidgets as qtw

from Ui.BoardsUi import Ui_MainWindow as boards

from widgets import CheckBox

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

    def __init__(self, file_manager, parent=None):
        super().__init__(parent=parent)

        # Definition of attributes
        self.parent = parent
        self.boards_ui = boards()
        self.file_manager = file_manager
        self.check_boxes = []

        self.boards_ui.setupUi(self)

        # Connecting buttons
        self.update_labels()

        self.show()

    def update_labels(self):
        """
        Updates the libraries that are on display.
        """

        for name in list(self.file_manager.boards.keys()):
            versions = self.file_manager.get_versions(name, self.file_manager.boards)
            check_box = CheckBox(name, self.file_manager.get_html(
                name, self.file_manager.boards), versions, parent=self)
            self.check_boxes.append(check_box.horizontal_layout)
            self.boards_ui.boards.addLayout(self.check_boxes[-1])

    def install(self, version, name):
        """
        calls the actuall install function on a thread

        Args:
            version (string): the selected version to install
            name (string): the name of the library to install   
        """
        architecture = self.file_manager.boards[name]["architecture"]
        self.parent.cli_manager.communicate(
            f"core install \"{architecture}@{version}\"")

        print(self.parent.cli_manager.get_cmd_output(
            f"board search"))