"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import shutil
import platform


class FileManager():
    """
    All processing to do with OS information such as file directorys, saves and more
    """

    def __init__(self):

        self.user = os.getlogin()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.operating_system = platform.system()

        # Initialise for each OS
        if self.operating_system == "Windows":
            self.sep = "\\"
            inc = "C:"
        elif self.operating_system == "Darwin":
            self.sep = "/"
            inc = ""
        elif self.operating_system == "Linux":
            self.sep = "/"
            inc = ""
        else:
            raise Exception("Invalis OS. Shutting down.")

        # Definitions for frequently used paths
        self.documents_path = f"{inc}{self.sep}Users{self.sep}{self.user}{self.sep}Documents"
        self.sidekick_path = f"{self.documents_path}{self.sep}SideKick"
        self.projects_path = f"{self.sidekick_path}{self.sep}SK Projects"
        self.libraries_path = f"{self.sidekick_path}{self.sep}Libraries"
        self.saves_path = f"{self.sidekick_path}{self.sep}SavedData"
        self.boards_path = f"{self.path}{self.sep}Settings{self.sep}boards.csv"
        self.settings_path = f"{self.path}{self.sep}Settings{self.sep}settings.txt"
        self.arduino_lib_path = f"{inc}{self.sep}Users{self.sep}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}library_index.json"

        # Creates directories if not already
        self.create_sidekick_file()
        self.create_sub_sidekick_files()

        # Checks for the SideKick libraries
        if len(os.listdir(self.libraries_path)) == 0:
            self.move_libraries()

    def create_sidekick_file(self):
        """
        Creates sidekick directory in documents if it does not already exist
        """

        directories = os.listdir(self.documents_path)
        if "SideKick" not in directories:
            os.mkdir(self.sidekick_path)

    def create_sub_sidekick_files(self):
        """
        Creates SideKick sub directories (SK Projects, SavedData, Libraries) if
        they do not already exist.
        """

        directories = os.listdir(self.sidekick_path)

        if "SK Projects" not in directories:
            os.mkdir(self.projects_path)
        if "SavedData" not in directories:
            os.mkdir(self.saves_path)
        if "Libraries" not in directories:
            os.mkdir(self.libraries_path)

    def move_libraries(self):
        """
        If the ConsciOS libraries are not present, then we ned to copy them from ConsciOS.
        TODO fix returns
        """

        conscios_folder = len(os.listdir(f"{self.path}{self.sep}ConsciOS"))

        if not conscios_folder:
            print("ERROR: The ConsciOS is non-existent!")
            return

        source = f"{self.path}{self.sep}ConsciOS"
        destination = f"{self.libraries_path}{self.sep}libraries"
        shutil.copytree(source, destination)

    def get_all_boards(self):
        """
        Gets all supported boards from the "./Ui/boards.csv".

        Returns:
            dictionary: the list of supported boards
        """

        board_dict = {}

        with open(self.boards_path, "r", encoding="UTF-8") as boards:
            for line in boards:
                names = line.split(", ")
                board_dict[names[0]] = names[1].strip()

        return board_dict

    def get_all_projects(self):
        """
        Gets all projects in the "SK Projects" folder.

        Returns:
            list: a list of all the projects
        """

        return os.listdir(self.projects_path)

    def add_new_project(self, name):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file

        TODO support new projects on enter key

        Args:
            name (string): the name of the new project from the line edit
        """

        if name in os.listdir(self.projects_path):
            return

        source = f"{self.path}{self.sep}ConsciOS{self.sep}Source"
        destination = f"{self.projects_path}{self.sep}{name}"
        shutil.copytree(source, destination)

        os.rename(f"{self.projects_path}{self.sep}{name}{self.sep}Source.ino",
                  f"{self.projects_path}{self.sep}{name}{self.sep}{name}.ino")

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

        project_path = f"{self.projects_path}{self.sep}{project}{self.sep}{project}.ino"

        compile_msg = f"\"{self.path}{self.sep}Externals{self.sep}arduino-cli.exe\" \
compile --fqbn {board} \"{project_path}\""

        upload_msg = f"\"{self.path}{self.sep}Externals{self.sep}arduino-cli.exe\" \
upload -p {port} --fqbn {board} \"{project_path}\""

        return [compile_msg, upload_msg]

    def save_options(self, board, project):
        """
        Saves selected options in drop downs to the settings.txt file so
        that the user doesn"t need to keep selecting drop downs on startup

        Args:
            board (string): the board type e.g. SK_Stem, Teensy4.1
            project (string): the current project selected
        """

        with open(self.settings_path, "r", encoding="UTF-8") as settings_file:

            settings = settings_file.readlines()

        for item in settings:

            if "Board: " in item:
                board_index = settings.index(item)

            if "Project: " in item:
                project_index = settings.index(item)

        settings[board_index] = f"Board: {board}\n"
        settings[project_index] = f"Project: {project}\n"

        with open(self.settings_path, "w", encoding="UTF-8") as settings_file:
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

        with open(self.settings_path, "r", encoding="UTF-8") as settings:

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
