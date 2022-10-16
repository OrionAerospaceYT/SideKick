"""
This file!
"""

import os
import shutil


class FileManager():
    """
    This class deals with creating and deleting files
    """

    def __init__(self):
        self.file = None
        self.user = os.getlogin()
        self.cwd = os.getcwd()

        self.create_sidekick_file()
        self.create_sub_sidekick_files()

    def create_sidekick_file(self):
        """Creates the SideKick directory in documents"""

        directories = os.listdir(f"C:/Users/{self.user}/Documents")
        if "SideKick" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick")

    def create_sub_sidekick_files(self):
        """Creats SideKick sub directories"""

        directories = os.listdir(f"C:/Users/{self.user}/Documents/SideKick")
        if "SK Projects" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        if "SavedData" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData')
        if "Libraries" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/Libraries')

            source = './ConsciOS/libraries'
            destination = f'C:/Users/{self.user}/Documents/SideKick/Libraries/libraries'
            shutil.copytree(source, destination)

    def get_all_boards(self):
        """Returns dictionary of devices"""

        board_dict = {}
        with open("./Ui/boards.csv", "r", encoding='UTF-8') as boards:
            for line in boards:
                names = line.split(", ")
                board_dict[names[0]] = names[1].strip()

        return board_dict

    def get_all_projects(self):
        """Returns all project directories except for Libraries"""

        projects = os.listdir(
            f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        return projects

    def add_new_project(self, name):
        """"Adds new projects when "new project"""

        if name in os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects"):
            return 0

        source = './ConsciOS/Source'
        destination = f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}'
        shutil.copytree(source, destination)

        os.rename(f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/Source.ino',
                  f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/{name}.ino')
        return 1

    def start_new_save(self):
        """Starts a new save file, should be called each time a new device is connected"""

        num_of_saves = len(os.listdir(
            f'C:/Users/{self.user}/Documents/SideKick/SavedData'))

        self.file = open(
            f"C:/Users/{self.user}/Documents/SideKick/SavedData/Save{num_of_saves + 1}",
            'w+',
            encoding='UTF-8')

    def save_terminal_data(self, data):
        """Saves data to file for users to read later"""
        self.file.write(f'{data}\n')
