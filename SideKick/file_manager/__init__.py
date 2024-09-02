"""
When the library_module is imported - the FileManager class is included by default.
"""
import os
import shutil
import platform

from SideKick.globals import SIZES_IN_QSS
from SideKick.globals import DEFAULT_SETTINGS, DEFAULT_BOARDS

from SideKick.file_manager.save_manager import SaveManager
from SideKick.file_manager.json_managers import JsonLibraryManager, JsonBoardsManager

class FileManager(JsonLibraryManager, JsonBoardsManager):
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

    def __init__(self, path, dev=False, consci_os_path=""):
        operating_system = platform.system()

        self.user = os.getenv("USER") or os.getenv("USERNAME")
        self.path = path
        self.save_manager = SaveManager()
        self.dev = dev
        self.consci_os_path = consci_os_path
        self.current_project = ""

        self.board_names = []

        # Initialise for each OS
        if operating_system == "Windows":
            self.arduino_cli = "arduino-cli-windows.exe"
            self.sep = "\\"
            inc = "C:\\Users\\"
            documents = "Documents"

            arduino15_path = f"{inc}{self.user}{self.sep}AppData{self.sep}Local{self.sep}Arduino15\
{self.sep}"

        elif operating_system == "Darwin":
            self.arduino_cli = "arduino-cli-mac"
            self.sep = "/"
            inc = "/Users/"
            documents = "documents"

            arduino15_path = f"{inc}{self.user}{self.sep}Library{self.sep}Arduino15{self.sep}"

        elif operating_system == "Linux":

            self.arduino_cli = "arduino-cli-linux.sh"
            self.sep = "/"
            inc = "/home/"
            documents = "Documents"

            arduino15_path = f"{inc}{self.user}{self.sep}.arduino15{self.sep}"

        else:
            raise OSError("Invalis OS. Shutting down.")

        self.paths = {"documents" : f"{inc}{self.user}{self.sep}{documents}",
"boards" : f"{self.path}{self.sep}Settings{self.sep}boards.csv",
"settings" : f"{self.path}{self.sep}Settings{self.sep}settings.txt",
"settings_path" : f"{self.path}{self.sep}Settings",
"arduino" : f"{self.path}{self.sep}Externals{self.sep}{self.arduino_cli}",
"actuator" : f"{self.path}{self.sep}Examples{self.sep}Actuators_Test{self.sep}Actuators_Test.ino",
"images" : f"{self.path}{self.sep}Images{self.sep}".replace(f"{self.sep}", "/"),
"stylesheet" : f"{self.path}{self.sep}Ui{self.sep}StyleSheet{self.sep}stylesheet.qss"}

        self.paths["sidekick"] = f"""{self.paths["documents"]}{self.sep}SideKick"""
        self.paths["projects"] = f"""{self.paths["sidekick"]}{self.sep}Projects"""
        self.paths["libraries"] = f"""{self.paths["sidekick"]}{self.sep}Libraries"""

        self.save_manager.save_folder_path = f"""{self.paths["sidekick"]}{self.sep}Saves"""
        self.save_manager.sep = self.sep

        # Creates directories if not already
        self.create_sidekick_files()
        self.create_sub_sidekick_files()

        # Checks if the GUI is being used in dev mode
        if dev:
            print("<<< WARNING >>> THIS APP IS CURRENTLY IN DEVELOPMENT MODE")
            self.move_libraries(consci_os_path)
        elif len(os.listdir(self.paths["libraries"])) == 0:
            self.move_libraries()

        self.load_boards_csv()
        self.update = True

        super(FileManager, self).__init__(arduino15_path + "library_index.json")
        super(JsonLibraryManager, self).__init__(arduino15_path, "package_", "_index.json")

    def create_sidekick_files(self):
        """
        Creates sidekick directory in documents if it does not already exist
        """
        directories = os.listdir(self.paths["documents"])
        if "SideKick" not in directories:
            os.mkdir(self.paths["sidekick"])

        directories = os.listdir(self.path)
        if "Settings" not in directories:
            os.mkdir(self.paths["settings_path"])

    def create_sub_sidekick_files(self):
        """
        Creates SideKick sub directories (Projects, SavedData, Libraries) if
        they do not already exist.
        """

        directories = os.listdir(self.paths["sidekick"])

        if "Projects" not in directories:
            os.mkdir(self.paths["projects"])
        if "Saves" not in directories:
            os.mkdir(self.save_manager.save_folder_path)
        if "Libraries" not in directories:
            os.mkdir(self.paths["libraries"])

        directories = os.listdir(self.paths["settings_path"])

        if "settings.txt" not in directories:
            with open(self.paths["settings"], "a", encoding="UTF-8") as settings:
                settings.write(DEFAULT_SETTINGS)

        if "boards.csv" not in directories:
            with open(self.paths["boards"], "a", encoding="UTF-8") as _:
                pass
            self.update_boards()

    def move_source(self, raw_source):
        """
        If the GUI is in dev mode, replace the reference to the source code
        for new projects
        """

        try:
            shutil.rmtree(f"{self.path}{self.sep}ConsciOS{self.sep}libraries")
            shutil.rmtree(f"{self.path}{self.sep}ConsciOS{self.sep}Source")
        except FileNotFoundError:
            pass

        source = f"{raw_source}{self.sep}libraries"
        destination = f"{self.path}{self.sep}ConsciOS{self.sep}libraries"
        shutil.copytree(source, destination)

        source = f"{raw_source}{self.sep}Source"
        destination = f"{self.path}{self.sep}ConsciOS{self.sep}Source"
        shutil.copytree(source, destination)

    def move_libraries(self, source=None):
        """
        If the ConsciOS libraries are not present, then we need to copy them from ConsciOS
        Or if the app is being used in development mode

        Args:
            source (str): the source to the new libraries
        """

        if "libraries" not in os.listdir(self.paths["libraries"]):
            os.mkdir(f"""{self.paths["libraries"]}{self.sep}libraries""")

        destination = f"""{self.paths["libraries"]}{self.sep}libraries"""

        if source is None:
            source = f"{self.path}{self.sep}ConsciOS{self.sep}libraries"
        else:
            source += f"{self.sep}libraries"

        for library in os.listdir(source):
            if "." in library:
                continue

            if library in os.listdir(destination):
                shutil.rmtree(f"{destination}{self.sep}{library}")

            shutil.copytree(f"{source}{self.sep}{library}", f"{destination}{self.sep}{library}")

    def get_all_projects(self):
        """
        Gets all projects in the "SK Projects" folder.

        Returns:
            list: a list of all the projects
        """
        return os.listdir(self.paths["projects"])

    def get_all_saves(self):
        """
        Gets all saves in the "SavedData" folder.

        Returns:
            list: a list of all saves
        """
        return os.listdir(self.save_manager.save_folder_path)

    def add_new_project(self, project_dir):
        """
        Adds new projects when new project is clicked.
        Creates a new file, copies the source reference, then renames the .ino file

        Args:
            name (string): the name of the new project from the line edit
        """
        project_dir = project_dir.replace("/", self.sep)

        source = f"{self.path}{self.sep}ConsciOS{self.sep}Source"
        destination = f"{project_dir}"

        shutil.copytree(source, destination)

        os.rename(f"{project_dir}{self.sep}Source.ino",
                  f"{project_dir}{self.sep}{project_dir.split(self.sep)[-1]}.ino")

        self.set_current_project(
            f"{project_dir}{self.sep}{project_dir.split(self.sep)[-1]}.ino",
            True )

    def remove_project(self, name):
        """
        Deletes project

        Args:
            name (str): the project name
        """
        shutil.rmtree(f"""{self.paths["projects"]}{self.sep}{name}""")

    def get_cli_path(self):
        """
        Returns:
            string: the path to arduino cli
        """
        return f"\"{self.path}{self.sep}Externals{self.sep}{self.arduino_cli}\""

    def set_dev_file(self):
        """
        Compiles and uploads the script
        sets the current_project to the dev project
        """

        if self.dev:
            self.move_libraries(f"{self.consci_os_path}")
            self.current_project = f"{self.consci_os_path}{self.sep}Source{self.sep}Source.ino"

    def save_options(self, board, project, lite):
        """
        Saves selected options in drop downs to the settings.txt file so
        that the user doesn"t need to keep selecting drop downs on startup

        Args:
            board (string): the board type e.g. SK_Stem, Teensy4.1
            project (string): the current project selected
        """

        with open(self.paths["settings"], "r", encoding="UTF-8") as settings_file:

            settings = settings_file.readlines()

        for item in settings:

            if "Board: " in item:
                board_index = settings.index(item)
                settings[board_index] = f"Board: {board}\n"

            elif "Project: " in item:
                project_index = settings.index(item)
                settings[project_index] = f"Project: {project}\n"

            elif "Lite: " in item:
                lite_index = settings.index(item)
                settings[lite_index] = f"Lite: {lite}\n"

        with open(self.paths["settings"], "w", encoding="UTF-8") as settings_file:
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
        lite = None

        in_drop_down_section = False

        with open(self.paths["settings"], "r", encoding="UTF-8") as settings:

            for line in settings:

                if "Drop down options:" in line:
                    in_drop_down_section = True

                if in_drop_down_section:
                    if "Board: " in line:
                        board = line.replace("Board: ", "")
                        board = board.strip()
                    elif "Project: " in line:
                        project = line.replace("Project: ", "")
                        project = project.strip()
                    elif "Lite: " in line:
                        lite = line.replace("Lite: ", "")
                        lite = lite.strip()
                        if lite == "False":
                            lite = False
                        else:
                            lite = True

        if lite is None:
            with open(self.paths["settings"], "a", encoding="UTF-8") as settings:
                settings.write("Lite: False")
                lite = False

        if not os.path.exists(project):
            if len(os.listdir(self.paths["projects"])) > 0:
                project_name = os.listdir(self.paths["projects"])[0]
                project = f"""{self.paths["projects"]}{self.sep}{project_name}"""
                project += f"{self.sep}{project_name}.ino"
                project = project.replace("\\", "/")
            else:
                project = ""

        return board, project, lite

    def load_boards_csv(self):
        """
        Gets all of the boards from ./Ui/boards.csv so
        that they can be displayed on the GUI.
        """

        with open(self.paths["boards"], "r", encoding="UTF-8") as boards:
            for line in boards:
                self.board_names.append(line.strip().split(", "))

    def set_current_project(self, file_path, manual=False):
        """
        Sets the current_project variable

        Args:
            file_path (str): the file path to the .ino file
        """

        if manual:
            self.current_project = file_path.replace("\\", "/")
            return

        try:
            if self.sep != "\\":
                self.current_project = file_path.split(self.sep)[-2]
            else:
                self.current_project = file_path.split("/")[-2]

            self.current_project = file_path
        except IndexError:
            pass

    def parsed_project_name(self):
        """
        Removes all of the file directory info from the name

        Returns:
            str: the name to be displayed on the GUI
        """

        try:
            if self.sep != "\\":
                name = self.current_project.split(self.sep)[-2]
            else:
                name = self.current_project.split("/")[-2]
        except IndexError:
            name = ""

        return name

    def set_all_boards(self, cli_manager:str):
        """
        Args:
            cli_magaer (CliManager) : the cli manager that runs commands
        """
        self.board_names = DEFAULT_BOARDS
        boards_str = cli_manager.get_cmd_output("board listall")

        boards_list = []
        for item in boards_str.decode("UTF-8").split("\n"):
            if item:
                boards_list.append(item.strip().split("  "))

        for item in boards_list:
            self.board_names.append([x for x in item if x])

        self.board_names.pop(2)

        self.update_boards()

    def update_boards(self):
        """
        Updates the boards.csv file to include all of the new boards
        """

        self.update = True

        with open(self.paths["boards"], "w", encoding="UTF-8") as boards:
            for board in self.board_names:
                if len(board) > 1:
                    boards.write(f"{board[0]}, {board[1]}\n")

    def get_examples(self):
        """
        Get all of the arduino sketches from the libraries path.

        Returns:
            list: the fild directories of the arduino examples.
        """
        libraries_path = self.paths["libraries"]+f"{self.sep}libraries"
        files = os.listdir(libraries_path)
        examples = []
        for file in files:
            if os.path.isfile(libraries_path+f"{self.sep}{file}"):
                continue
            if "examples" not in os.listdir(libraries_path+f"{self.sep}{file}"):
                continue
            examples.append(file)
        return examples

    def change_size_stylesheet(self, increase:bool):
        """
        Either increases or decreases the size of the font on the GUI.
        """
        with open(
            self.paths["stylesheet"],
            "r",
            encoding="UTF-8") as sizes:
            scale = float(sizes.readline())
            stylesheet = sizes.read()

        if increase:
            scale += 0.1
            scale = round(scale, 1)
            if scale == 0.7:
                scale = 0.8
            elif scale == 1.2:
                scale = 1.3
            elif scale == 1.7:
                scale = 1.8
            elif scale == 2.1:
                scale = 2.2
            scale = min(scale, 2.3)
        else:
            scale -=0.1
            scale = round(scale, 1)
            if scale == 0.7:
                scale = 0.6
            elif scale == 1.2:
                scale = 1.1
            elif scale == 1.7:
                scale = 1.6
            elif scale == 2.1:
                scale = 2.0
            scale = max(scale, 0.5)

        with open(
            self.paths["stylesheet"],
            "w",
            encoding="UTF-8") as sizes:
            scale = round(scale, 1)
            sizes.write(str(scale)+"\n"+stylesheet)

    def get_scale(self) -> float:
        """
        Gets the scale from the stylesheet.
        """
        with open(
            self.paths["stylesheet"],
            "r",
            encoding="UTF-8") as scale:
            return float(scale.readline())

    def get_size_stylesheet(self) -> tuple:
        """
        Gets and formats the size style guide for the GUI.
        """

        with open(
            self.paths["stylesheet"],
            "r",
            encoding="UTF-8") as sizes:
            scale = float(sizes.readline())
            stylesheet = sizes.read()

        stylesheet = self.fix_ui_path(stylesheet)

        for size in SIZES_IN_QSS:
            stylesheet = stylesheet.replace(str(size) + "px", str(int(size*scale)) + "px")

        return stylesheet, scale

    def fix_ui_path(self, qss:str) -> str:
        """
        Args:
            qss(str): the qss which has a relative Ui/* path
        
        Returns:
            str: the fixed qss with a proper path
        """
        return qss.replace("Ui", self.paths["images"])

    def get_loading_screen(self) -> str:
        """
        Returns:
            str: the directory of the loading screen.
        """
        path = self.paths["images"]
        return f"{path}Loading_Screen.png"

    def get_icon(self) -> str:
        """
        Returns:
            str: the directory of the SideKick icon.
        """
        path = self.paths["images"]
        return f"{path}SideKick.ico"
