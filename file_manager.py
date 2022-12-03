"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import shutil
import platform


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
        self.operating_system = platform.system()
        if self.operating_system == 'Windows':
           self.bsfs = '\\' 
           self.inc = 'C:'
        elif self.operating_system == 'Darwin':
            self.bsfs = '/'
            self.inc = ''
        elif self.operating_system == 'Linux':
            self.bsfs = '/'
            self.inc = ''
        else:
            print("invalid os")
            # Raise error
        self.create_sidekick_file()
        self.create_sub_sidekick_files()

        if len(os.listdir(f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}Libraries')) <= 0:
            self.move_libraries()

    def create_sidekick_file(self):
        """
        Creates the SideKick directory in documents if it dos not exist
        """

        directories = os.listdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents")
        if "SideKick" not in directories:
            os.mkdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick")

    def create_sub_sidekick_files(self):
        """
        Creates SideKick sub directories (SK Projects, SavedData, Libraries)
        """

        directories = os.listdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick")

        if "SK Projects" not in directories:
            os.mkdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects")
        if "SavedData" not in directories:
            os.mkdir(f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SavedData')
        if "Libraries" not in directories:
            os.mkdir(f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}Libraries')

    def move_libraries(self):
        """
        Copies the sidekick ConsciOS to the libraries folder
        """

        conscios_folder = len(os.listdir("ConsciOS"))

        if not conscios_folder:
            print("ERROR: The ConsciOS is non-existent!")
            return

        source = 'ConsciOS{self.bsfs}libraries'
        destination = f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}Libraries{self.bsfs}libraries'
        shutil.copytree(source, destination)

    def get_all_boards(self):
        """
        Returns dictionary of valid devices
        Based off of the boards.csv file
        """

        board_dict = {}

        with open(".{self.bsfs}Ui{self.bsfs}boards.csv", "r", encoding='UTF-8') as boards:
            for line in boards:
                names = line.split(", ")
                board_dict[names[0]] = names[1].strip()

        return board_dict

    def get_all_projects(self):
        """
        Returns all project directories except for Libraries
        """

        return os.listdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects")

    def add_new_project(self, name):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file

        Args:
            name (string): the name of the new project from the line edit
        """

        if name in os.listdir(f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects"):
            return

        source = '.{self.bsfs}ConsciOS{self.bsfs}Source'
        destination = f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects{self.bsfs}{name}'
        shutil.copytree(source, destination)

        os.rename(f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects{self.bsfs}{name}{self.bsfs}Source.ino',
                  f'{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects{self.bsfs}{name}{self.bsfs}{name}.ino')

    def compile_and_upload_commands(self, port, project, board):
        """
        Compiles and uploads the script

        Args:
            port (string): the com port the device is connected to e.g. "COM1"
            board (string): the type of sidekick{self.bsfs}teensy{self.bsfs}arduino board
            project (string): the name of the project to upload
        Returns:
            list: with [compile (string), upload (string)]
        """

        project_path = f"{self.inc}{self.bsfs}Users{self.bsfs}{self.user}{self.bsfs}Documents{self.bsfs}SideKick{self.bsfs}SK Projects{self.bsfs}\
{project}{self.bsfs}{project}.ino"

        compile_msg = f"\"{self.cwd}{self.bsfs}Externals{self.bsfs}arduino-cli.exe\" compile --fqbn \
{board} \"{project_path}\""

        upload_msg = f"\"{self.cwd}{self.bsfs}Externals{self.bsfs}arduino-cli.exe\" \
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
