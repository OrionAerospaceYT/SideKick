"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import shutil
import platform
import json

class SaveManager():
    """
    loads and saves data to the saves file
    """

    def __init__(self):
        self.record_status = False
        self.prev_record_status = False
        self.save_folder_path = ""
        self.sep = ""
        self.prev_save_data = []

    def create_new_file(self):
        """
        creates a new save file
        """
        num_of_saves = len(os.listdir(self.save_folder_path))
        with open(f"{self.save_folder_path}{self.sep}Save{num_of_saves+1}.txt", "w",
                    encoding="UTF-8"):
            pass

    def save_data(self, save_data):
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
            for data in save_data:
                save.write(data)
                save.write("\n")

        self.prev_record_status = True

    def stop_save(self):
        """
        sets record_status to false
        """
        self.record_status = False
        self.prev_record_status = False

    def get_saved_data(self, file_dir):
        """
        loads the file and gets all data from it

        Returns:
            list: the saved raw data
        """
        with open(file_dir, "r", encoding="UTF-8") as save:
            data = save.readlines()

        return [item.strip() for item in data]


class HtmlGenerator():
    """
    Holds the functions which generate html for JsonLibraryManager and
    JsonBoardsManager.
    """

    def get_versions(self, name, my_dict):
        """
        Returns all of the versions that are avaliable.
        """

        return list(my_dict[name]["version"])

    def get_title(self, name):
        """
        Returns the formatting for a title on the QTextBrowser of libraries
        that can be installed.

        Args:
            name (string): the text for the title (name)
        """

        return f"<h1><p style=\"color:#00f0c3; font-size:20px\">{name}</p></h1><br>"

    def get_link(self, name, link):
        """
        Returns the html link for categories which are links.

        Args:
            name (string): the link
        """

        return f"<a style=\"color:#8ab4f8\" href={link}>{name}</a><br>"

    def get_paragraph(self, name, text):
        """
        Makes a paragraph for each sub category

        Args:
            name (string): the name of the category
            text (string): the description
        """
        return f"<p>{name}: {text}</p>"

    def get_list_paragraph(self, name, my_list):
        """
        Makes a paragraph for each sub category

        Args:
            name (string): the name of the category
            list (list): the description
        """
        string = f"<p>{name}:"
        for item in my_list:
            string += f"<br>{item}"
        return string

    def get_html(self, name, my_dict):
        """
        Formats the library text for the display on library manager options
        
        Args:
            name (str): the name of the dictionary item
            my_dict (dictionary): the dictionary to parse into html
        """
        html = ""

        for item in list(my_dict[name].keys()):
            if item in ("name", "architecture"):
                html = self.get_title(str(my_dict[name][item]))
            elif item in ("checksum", "version"):
                pass
            elif item in ("repository", "url", "website"):
                html += self.get_link(item, str(my_dict[name][item]))
            elif isinstance(my_dict[name][item], list):
                html += self.get_list_paragraph(item, my_dict[name][item])
            elif isinstance(item, str):
                html += self.get_paragraph(item, str(my_dict[name][item]))

        return html


class JsonLibraryManager(HtmlGenerator):
    """
    Json loader class that gets all information for the arduino
    library manager.
    """

    def __init__(self, path):

        self.lib_path = path
        self.libraries = {}
        self.load_libs()
        #self.get_info(list(self.libraries.keys())[0])

    def load_libs(self):
        """
        Loads all libraries from the library.json file in arduino15.
        """
        with open(self.lib_path, encoding="utf-8") as file:
            data = json.load(file)

        libraries = data.get("libraries")
        for library in libraries:
            if library["name"] in self.libraries:
                self.libraries[library["name"]]["version"].append(library["version"])
            else:
                self.libraries[library["name"]] = library
                self.libraries[library["name"]]["version"] = [
                    self.libraries[library["name"]]["version"]]

    def get_all_libraries(self, name):
        """
        Returns all keys with the name in them.

        Args:
            name (string): the keyword to look for in the name
        """

        keys = list(self.libraries.keys())

        libraries = []

        for key in keys:
            if name.lower() in key.lower():
                libraries.append(key)

        return libraries

class JsonBoardsManager(HtmlGenerator):
    """
    Processes and parses the boards json file.
    """
    def __init__(self, path):

        self.board_path = path
        self.boards = {}
        self.load_boards()

    def format_dict(self, input_dict):
        """
        Formats the dictionary into a better form to be displayed
        on the screen.

        Args:
            dict (dictionary) : The dictionary to be formatted
        """
        formatted_dict = {"architecture": input_dict["architecture"],
        "version": [input_dict["version"]],
        "url": input_dict["url"],
        "boards": [board["name"] for board in input_dict["boards"]]}

        return formatted_dict

    def load_boards(self):
        """
        Loads all libraries from the library.json file in arduino15.
        """

        with open(self.board_path, encoding="utf-8") as file:
            data = json.load(file)

        packages = data.get("packages")

        for package in packages:
            for board in package["platforms"]:
                if board["name"].startswith("[DEPRECATED"):
                    continue
                if board["name"] in self.boards:
                    self.boards[board["name"]]["version"].append(board["version"])
                else:
                    self.boards[board["name"]] = self.format_dict(board)


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

    def __init__(self, dev, consci_os_path):

        self.user = os.getlogin()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.operating_system = platform.system()
        self.save_manager = SaveManager()
        self.dev = dev
        self.consci_os_path = consci_os_path
        self.current_project = ""

        # Initialise for each OS
        if self.operating_system == "Windows":
            self.arduino_cli = "arduino-cli-windows.exe"
            self.sep = "\\"
            inc = "C:\\Users\\"
            documents = "Documents"

            arduino_lib_path = f"{inc}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}library_index.json"

            arduino_board_path = f"{inc}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}package_index.json"

        elif self.operating_system == "Darwin":
            self.arduino_cli = "arduino-cli-mac"
            self.sep = "/"
            inc = "/Users/"
            documents = "documents"

            arduino_lib_path = f"{inc}{self.user}{self.sep}\
Library{self.sep}Arduino15{self.sep}library_index.json"

            arduino_board_path = f"{inc}{self.user}{self.sep}\
Library{self.sep}Arduino15{self.sep}package_index.json"

        elif self.operating_system == "Linux":

            self.arduino_cli = "arduino-cli-linux.sh"
            self.sep = "/"
            inc = "/home/"
            documents = "Documents"

            arduino_lib_path = f"{inc}{self.user}{self.sep}.arduino15\
{self.sep}library_index.json"

            arduino_board_path = f"{inc}{self.user}{self.sep}.arduino15\
{self.sep}package_index.json"

        else:
            raise OSError("Invalis OS. Shutting down.")

        # Definitions for frequently used paths
        self.documents_path = f"{inc}{self.user}{self.sep}{documents}"
        self.sidekick_path = f"{self.documents_path}{self.sep}SideKick"
        self.projects_path = f"{self.sidekick_path}{self.sep}Projects"
        self.libraries_path = f"{self.sidekick_path}{self.sep}Libraries"
        self.boards_path = f"{self.path}{self.sep}Settings{self.sep}boards.csv"
        self.settings_path = f"{self.path}{self.sep}Settings{self.sep}settings.txt"
        self.arduino_path = f"{self.path}{self.sep}Externals{self.sep}{self.arduino_cli}"
        self.actuators_test = \
            f"{self.path}{self.sep}Examples{self.sep}Actuators_Test{self.sep}Actuators_Test.ino"
        self.save_manager.save_folder_path = f"{self.sidekick_path}{self.sep}Saves"
        self.save_manager.sep = self.sep

        # Creates directories if not already
        self.create_sidekick_file()
        self.create_sub_sidekick_files()

        # Checks if the GUI is being used in dev mode
        if dev:
            print("<<< WARNING >>> THIS APP IS CURRENTLY IN DEVELOPMENT MODE")
            self.move_libraries(consci_os_path)
        elif len(os.listdir(self.libraries_path)) == 0:
            self.move_libraries()

        super(FileManager, self).__init__(arduino_lib_path)
        super(JsonLibraryManager, self).__init__(arduino_board_path)

    def create_sidekick_file(self):
        """
        Creates sidekick directory in documents if it does not already exist
        """

        directories = os.listdir(self.documents_path)
        if "SideKick" not in directories:
            os.mkdir(self.sidekick_path)

    def create_sub_sidekick_files(self):
        """
        Creates SideKick sub directories (Projects, SavedData, Libraries) if
        they do not already exist.
        """

        directories = os.listdir(self.sidekick_path)

        if "Projects" not in directories:
            os.mkdir(self.projects_path)
        if "Saves" not in directories:
            os.mkdir(self.save_manager.save_folder_path)
        if "Libraries" not in directories:
            os.mkdir(self.libraries_path)

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
        If the ConsciOS libraries are not present, then we ned to copy them from ConsciOS
        Or if the app is being used in development mode

        Args:
            source (str): the source to the new libraries
        """

        if "libraries" not in os.listdir(self.libraries_path):
            os.mkdir(f"{self.libraries_path}{self.sep}libraries")

        destination = f"{self.libraries_path}{self.sep}libraries"

        if source is None:
            source = f"{self.path}{self.sep}ConsciOS{self.sep}libraries"
        else:
            source += f"{self.sep}libraries"

        for library in os.listdir(source):
            try:
                if library in os.listdir(destination):
                    shutil.rmtree(f"{destination}{self.sep}{library}")

                shutil.copytree(f"{source}{self.sep}{library}", f"{destination}{self.sep}{library}")
            except NotADirectoryError:
                pass

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
        shutil.rmtree(f"{self.projects_path}{self.sep}{name}")

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

        if not os.path.exists(project):
            if len(os.listdir(self.projects_path)) > 0:
                project_name = os.listdir(self.projects_path)[0]
                project = f"{self.projects_path}{self.sep}{project_name}"
                project += f"{self.sep}{project_name}.ino"
                project = project.replace("\\", "/")
            else:
                project = ""

        return board, project

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
