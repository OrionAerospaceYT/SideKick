"""
This file is responsible for handling all creation and
deletion of files.
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

        if len(os.listdir(f'C:/Users/{self.user}/Documents/SideKick/Libraries')) <= 0:
            self.move_libraries()

    def create_sidekick_file(self):
        """
        Creates the SideKick directory in documents if it dos not exist
        """

        directories = os.listdir(f"C:/Users/{self.user}/Documents")
        if "SideKick" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick")

    def create_sub_sidekick_files(self):
        """
        Creates SideKick sub directories (SK Projects, SavedData, Libraries)
        """

        directories = os.listdir(f"C:/Users/{self.user}/Documents/SideKick")

        if "SK Projects" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        if "SavedData" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData')
        if "Libraries" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/Libraries')

    def move_libraries(self):
        """
        Copies the sidekick ConsciOS to the libraries folder
        """

        conscios_folder = len(os.listdir("ConsciOS"))

        if not conscios_folder:
            print("ERROR: The ConsciOS is non-existent!")
            return

        source = 'ConsciOS/libraries'
        destination = f'C:/Users/{self.user}/Documents/SideKick/Libraries/libraries'
        shutil.copytree(source, destination)

    def get_all_boards(self):
        """
        Returns dictionary of valid devices
        Based off of the boards.csv file
        """

        board_dict = {}

        with open("./Ui/boards.csv", "r", encoding='UTF-8') as boards:
            for line in boards:
                names = line.split(", ")
                board_dict[names[0]] = names[1].strip()

        return board_dict

    def get_all_projects(self):
        """Returns all project directories except for Libraries"""

        return os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")

    def add_new_project(self, name):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file
        """

        if name in os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects"):
            return

        source = './ConsciOS/Source'
        destination = f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}'
        shutil.copytree(source, destination)

        os.rename(f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/Source.ino',
                  f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/{name}.ino')

    def start_new_save(self):
        """
        Starts a new save file, saves are called save[indx] and is a text file
        Files are saved in the users documents folder under Documents/SideKick/SavedData
        """

        num_of_saves = len(os.listdir(
            f'C:/Users/{self.user}/Documents/SideKick/SavedData'))

        self.file = open(
            f"C:/Users/{self.user}/Documents/SideKick/SavedData/Save{num_of_saves + 1}",
            'w+',
            encoding='UTF-8')

    def save_terminal_data(self, data):
        """Saves data to file for users to read later"""

        self.file.write(f'{data}\n')
