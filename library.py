"""
Library manager
"""
from manager import Manager, library_no_results, library_instructions

class LibraryManager(Manager):
    """
    Re-Write this docstring TODO
    """

    def __init__(self, parent=None):
        super().__init__("SideKick Library Manager", "library", True, parent)

        self.manager_ui.install.clicked.connect(self.install)
        self.manager_ui.search_bar.returnPressed.connect(self.update_labels)

        self.manager_ui.search_bar.setPlaceholderText("Search for your library here")

        self.manager_ui.selectable_items.addWidget(library_instructions())

        self.show()

    def get_search_term(self) -> str | None:
        """
        Checks that the search term the user has entered is valid
        """
        search_term = self.manager_ui.search_bar.text()
        if len(search_term) < 3:
            return None
        return search_term

    def update_labels(self):
        """
        Update the libraries which are on display for the user to select
        """
        self.clear_widgets()

        search_term = self.get_search_term()

        if not search_term:
            self.manager_ui.selectable_items.addWidget(library_instructions())
            return

        for name in self.file_manager.get_all_libraries(search_term):
            super().add_widget(name, self.file_manager.libraries)

        self.manager_ui.search_bar.setText("")

        if len(self.widgets) == 0:
            self.manager_ui.selectable_items.addWidget(library_no_results())

    def install(self):
        """
        Installs the correct library at the correct version
        """
        if self.selected == -1:
            return

        name = self.widgets[self.selected].name
        version = self.manager_ui.versions.currentText()

        self.parent.cli_manager.communicate(f"lib install \"{name}@{version}\"")
