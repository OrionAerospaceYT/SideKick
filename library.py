"""
Library manager
"""
from manager import Manager

class LibraryManager(Manager):
    """
    Re-Write this docstring TODO
    """

    def __init__(self, parent=None):
        super().__init__("SideKick Library Manager", "library", True, parent)

        self.manager_ui.install.clicked.connect(self.install)
        self.manager_ui.search_bar.returnPressed.connect(self.update_labels)

        self.manager_ui.search_bar.setPlaceholderText("Search for your library here")

        self.show()

    def update_labels(self):
        """
        Update the libraries which are on display for the user to select
        """
        self.clear_widgets()
        for name in self.file_manager.get_all_libraries(self.manager_ui.search_bar.text()):
            super().add_widget(name, self.file_manager.libraries)
        self.manager_ui.search_bar.setText("")

    def install(self):
        """
        Installs the correct library at the correct version
        """
        if self.selected == -1:
            return

        name = self.widgets[self.selected].name
        version = self.manager_ui.versions.currentText()

        self.parent.cli_manager.communicate(f"lib install \"{name}@{version}\"")
