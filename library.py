"""
Library manager
"""

from PyQt6 import QtWidgets as qtw

from Ui.LibraryUi import Ui_MainWindow as library

from widgets import CheckBox

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
            versions = self.file_manager.get_versions(name, self.file_manager.libraries)
            check_box = CheckBox(name, self.file_manager.get_html(
                name, self.file_manager.libraries), versions, parent=self)
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
