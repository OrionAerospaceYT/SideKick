"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import shutil
import platform

class SaveManager():
    """
    loads and saves data to the saves file
    """

    def __init__(self):
        self.record_status = False
        self.prev_record_status = False
        self.save_folder_path = ""
        self.sep = ""

    def create_new_file(self):
        """
        creates a new save file
        """
        num_of_saves = len(os.listdir(self.save_folder_path))
        with open(f"{self.save_folder_path}{self.sep}Save{num_of_saves+1}.txt", "w",
                    encoding="UTF-8"):
            pass

    def save_data(self, raw_data):
        """
        saves the raw data to the latest save_file

        Args:
            raw_data (str): the raw data from com device
        """
        self.record_status = True
        if self.record_status != self.prev_record_status:
            self.create_new_file()

        save_name = f"Save{len(os.listdir(self.save_folder_path))}.txt"
        save_path = f"{self.save_folder_path}{self.sep}{save_name}"

        with open(save_path, "a", encoding="UTF-8") as save:
            if raw_data:
                save.write(raw_data[-1])
                save.write("\n")

        self.prev_record_status = True

    def stop_save(self):
        """
        sets record_status to false
        """
        self.record_status = False
        self.prev_record_status = False

    def get_saved_data(self, file_name):
        """
        loads the file and gets all data from it

        Returns:
            list: the saved raw data
        """
        with open(f"{self.save_folder_path}{self.sep}{file_name}", "r", encoding="UTF-8") as save:
            data = save.readlines()

        return [item.strip() for item in data]


class FileManager():
    """
    All processing to do with OS information such as file directorys, saves and more

    Attributes:
        user (str): the logged in user to the system
        path (str): the path of the main file being run
        script_ending (str): exe or sh depending on OS
        operating_system (str): the operating system the app is run on
        sep (str): the seperator for file directories
        save_manager (SaveManager): the class responsible for saving
        paths (str): the different necessary paths

    Methods:
    """

    def __init__(self):

        self.user = os.getlogin()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.operating_system = platform.system()
        self.save_manager = SaveManager()

        # Initialise for each OS
        if self.operating_system == "Windows":
            self.script_ending = "exe"
            self.sep = "\\"
            inc = "C:\\Users\\"
        elif self.operating_system == "Darwin":
            self.script_ending = "sh"
            self.sep = "/"
            inc = ""
        elif self.operating_system == "Linux":
            self.script_ending = "sh"
            self.sep = "/"
            inc = "/home/"
        else:
            raise Exception("Invalis OS. Shutting down.")

        # Definitions for frequently used paths
        self.documents_path = f"{inc}{self.user}{self.sep}Documents"
        self.sidekick_path = f"{self.documents_path}{self.sep}SideKick"
        self.projects_path = f"{self.sidekick_path}{self.sep}SK Projects"
        self.libraries_path = f"{self.sidekick_path}{self.sep}Libraries"
        self.boards_path = f"{self.path}{self.sep}Settings{self.sep}boards.csv"
        self.settings_path = f"{self.path}{self.sep}Settings{self.sep}settings.txt"
        self.arduino_path = f"{self.path}{self.sep}Externals{self.sep}arduino-cli.{self.script_ending}"
        self.arduino_lib_path = f"{inc}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}library_index.json"

        self.save_manager.save_folder_path = f"{self.sidekick_path}{self.sep}SavedData"
        self.save_manager.sep = self.sep

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
            os.mkdir(self.save_manager.save_folder_path)
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

    def get_all_saves(self):
        """
        Gets all saves in the "SavedData" folder.

        Returns:
            list: a list of all saves
        """
        return os.listdir(self.save_manager.save_folder_path)

    def add_new_project(self, name):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file

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

    def remove_project(self, name):
        """
        Deletes project

        Args:
            name (str): the project name
        """
        shutil.rmtree(f"{self.projects_path}{self.sep}{name}")

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

        compile_msg = f"\"{self.path}{self.sep}Externals{self.sep}arduino-cli.{self.script_ending}\" \
compile --fqbn {board} \"{project_path}\""

        upload_msg = f"\"{self.path}{self.sep}Externals{self.sep}arduino-cli.{self.script_ending}\" \
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
