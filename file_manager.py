"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import shutil


class FileManager():
    """
    Handles all files and operating system
        Current working directory
        Checking for all sidekick files
        Saves data
        Creates new projects
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
        """
        Returns all project directories except for Libraries
        """

        return os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")

    def add_new_project(self, name):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file

        Args:
            name (string): the name of the new project from the line edit
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
        """
        Saves data to file for users to read later

        Args:
            data (string): the data to be saved to the new save file
        """

        self.file.write(f'{data}\n')

    def compile_and_upload_commands(self, port, project, board):
        """
        Compiles and uploads the script

        Args:
            port (string): the com port the device is connected to e.g. "COM1"
            board (string): the type of sidekick/teensy/arduino board
            project (string): the name of the project to upload
        Returns:
            list: with [compile (string), upload (string)]
        """

        project_path = f"C:/Users/{self.user}/Documents/SideKick/SK Projects/\
{project}/{project}.ino"

        compile_msg = f"\"{self.cwd}/Externals/arduino-cli.exe\" compile --fqbn \
{board} \"{project_path}\""

        upload_msg = f"\"{self.cwd}/Externals/arduino-cli.exe\" \
upload -p {port} --fqbn {board} \"{project_path}\""

        return [compile_msg, upload_msg]

    def save_options(self, board, project):
        """
        Saves selected options in drop downs to the settings.txt file so
        that the user doesn't need to keep selecting drop downs on startup

        Args:
            board (string): the board type e.g. SK_Stem, Teensy4.1
            project (string): the current project selected
        """

        with open("settings.txt", "r", encoding="UTF-8") as settings_file:

            settings = settings_file.readlines()

        for item in settings:

            if "Board: " in item:
                board_index = settings.index(item)

            if "Project: " in item:
                project_index = settings.index(item)

        settings[board_index] = f"Board: {board}\n"
        settings[project_index] = f"Project: {project}\n"

        with open("settings.txt", "w", encoding="UTF-8") as settings_file:
            settings_file.writelines(settings)

    def load_options(self):
        """
        Loads the saved options to set the drop down box items

        Returns:
            board (string): the board type e.g. SK_Stem, Teensy4.1
            project (string): the current project selected
        """

        board = None
        project = None

        in_drop_down_section = False

        with open("settings.txt", "r", encoding="UTF-8") as settings:

            for line in settings:

                if "Drop down options:" in line:
                    in_drop_down_section = True

                if in_drop_down_section:
                    if "Board: " in line:
                        board = line.replace("Board: ", "")
                        board = board.strip()
                    if "Project: " in line:
                        project = line.replace("Project: ", "")
                        project = project.strip()

        return board, project
