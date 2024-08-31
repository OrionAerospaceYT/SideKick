"""
Controls the gui which allows the user to install other boards    
"""

import threading

from SideKick.manager import Manager

class BoardsManager(Manager):
    """
    Re-Write this docstring TODO
    """

    def __init__(self, parent=None):
        super().__init__("SideKick Boards Manager", "board", parent=parent)

        self.manager_ui.install.clicked.connect(self.install)
        self.update_labels()

        self.show()

    def update_labels(self):
        """
        Updates the boards that are on display.
        """
        for name in list(self.file_manager.boards.keys()):
            super().add_widget(name, self.file_manager.boards)

    def install(self):
        """
        Calls the actuall install function on a thread.
        """
        if self.selected == -1:
            return

        name = self.widgets[self.selected].name
        version = self.manager_ui.versions.currentText()
        architecture = self.file_manager.boards[name]["architecture"]

        command = f"core install \"{architecture}@{version}\""

        self.parent.cli_manager.communicate(command)
        threaded_wait = threading.Thread(target=self.wait_to_update_boards, args=(command,),)
        threaded_wait.start()

    def wait_to_update_boards(self, cmd):
        """
        Waits for the install command to be run before
        """
        while (cmd in self.cli_manager.commands.keys()) or self.cli_manager.running:
            pass
        self.file_manager.set_all_boards(self.cli_manager)
