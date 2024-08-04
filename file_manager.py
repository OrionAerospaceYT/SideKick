"""
This file is responsible for handling all creation and
deletion of files.
"""

import os
import re
import shutil
import platform
import json

from PyQt5 import QtWidgets as qtw

from globals import GRAPH_BEGINNING, GRAPH_ENDING

DEFAULT_BOARDS = [["Select Board", "None"],
                  ["SK Stem", "arduino:mbed_rp2040:pico"]]

DEFAULT_SETTINGS = """
Drop down options:\n
Board: Select Board\n
Project: None\n
"""

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
        with open(f"{self.save_folder_path}{self.sep}Save{num_of_saves+1}.sk", "w",
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

        save_name = f"Save{len(os.listdir(self.save_folder_path))}.sk"
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

    def parse_line(self, line:str) -> list:
        """
        Returns:
            list: the terminal data
            list: the graph_data
            bool: the recording status
        """
        terminal_data = ""
        graph_data = []

        line = line.replace("\n", "")

        graph_data = re.findall(f"{GRAPH_BEGINNING}.*?{GRAPH_ENDING}", line)

        for indx, item in enumerate(graph_data):
            graph_data[indx] = item.replace(GRAPH_BEGINNING, "").replace(GRAPH_ENDING, "")

        terminal_data = re.sub(f'{GRAPH_BEGINNING}.*?{GRAPH_ENDING}', '', line)

        if not terminal_data:
            terminal_data = None
        if not graph_data:
            graph_data = None

        return terminal_data, graph_data

    def export_save(self, file_dir:str, new_name:str):
        """
        Convert the sidekick data to a .csv file for the user.
        """
        output = "Terminal,Graphs\n"

        with open(file_dir, "r", encoding="UTF-8") as my_file:
            for line in my_file:
                parsed_line = self.parse_line(line)
                if parsed_line[0] is None:
                    output += ","
                else:
                    output += parsed_line[0] + ","
                if parsed_line[1] is None:
                    output += ","
                else:
                    for graph in parsed_line[1]:
                        output += graph + ","
                output += "\n"

        try:
            with open(f"{new_name}", "w", encoding="UTF-8") as my_file:
                my_file.write(output)
        except PermissionError:
            qtw.QMessageBox.critical(None,
                                        "Permission error", 
                                        "Could not save - file already in use!",
                                        qtw.QMessageBox.Cancel)

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
                    board["architecture"] = package["name"] + ":" + board["architecture"]
                    self.boards[board["name"]] = self.format_dict(board)
                    self.boards[board["name"]].update({"maintainer":package["maintainer"]})


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

        operating_system = platform.system()

        self.user = os.getlogin()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.save_manager = SaveManager()
        self.dev = dev
        self.consci_os_path = consci_os_path
        self.current_project = ""

        self.board_names = DEFAULT_BOARDS

        # Initialise for each OS
        if operating_system == "Windows":
            self.arduino_cli = "arduino-cli-windows.exe"
            self.sep = "\\"
            inc = "C:\\Users\\"
            documents = "Documents"

            arduino_lib_path = f"{inc}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}library_index.json"

            arduino_board_path = f"{inc}{self.user}{self.sep}\
AppData{self.sep}Local{self.sep}Arduino15{self.sep}package_index.json"

        elif operating_system == "Darwin":
            self.arduino_cli = "arduino-cli-mac"
            self.sep = "/"
            inc = "/Users/"
            documents = "documents"

            arduino_lib_path = f"{inc}{self.user}{self.sep}\
Library{self.sep}Arduino15{self.sep}library_index.json"

            arduino_board_path = f"{inc}{self.user}{self.sep}\
Library{self.sep}Arduino15{self.sep}package_index.json"

        elif operating_system == "Linux":

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

        self.paths = {"documents" : f"{inc}{self.user}{self.sep}{documents}",
"boards" : f"{self.path}{self.sep}Settings{self.sep}boards.csv",
"settings" : f"{self.path}{self.sep}Settings{self.sep}settings.txt",
"settings_path" : f"{self.path}{self.sep}Settings",
"arduino" : f"{self.path}{self.sep}Externals{self.sep}{self.arduino_cli}",
"actuator" : f"{self.path}{self.sep}Examples{self.sep}Actuators_Test{self.sep}Actuators_Test.ino"}

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

        super(FileManager, self).__init__(arduino_lib_path)
        super(JsonLibraryManager, self).__init__(arduino_board_path)

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

    def save_options(self, board, project):
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

            if "Project: " in item:
                project_index = settings.index(item)
                settings[project_index] = f"Project: {project}\n"

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

        in_drop_down_section = False

        with open(self.paths["settings"], "r", encoding="UTF-8") as settings:

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
            if len(os.listdir(self.paths["projects"])) > 0:
                project_name = os.listdir(self.paths["projects"])[0]
                project = f"""{self.paths["projects"]}{self.sep}{project_name}"""
                project += f"{self.sep}{project_name}.ino"
                project = project.replace("\\", "/")
            else:
                project = ""

        return board, project

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

    def set_all_boards(self, cli_manager:str) -> list:
        """
        Args:
            cli_magaer (CliManager) : the cli manager that runs commands

        Returns:
            list : the list of all boards installed
        """

        boards_str = cli_manager.get_cmd_output("board listall")

        boards_list = boards_str.decode("UTF-8").split("\n")
        boards_list = [item.strip().split("  ") for item in boards_list if item]

        all_boards = []

        for item in boards_list:
            all_boards.append([x for x in item if x])

        all_boards.pop(0)

        for board in reversed(DEFAULT_BOARDS):
            all_boards.insert(0, board)

        self.board_names = all_boards

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
            f".{self.sep}Ui{self.sep}size_guide.qss",
            "r",
            encoding="UTF-8") as sizes:
            scale = float(sizes.readline())
            stylesheet = sizes.read()

        if increase:
            scale += 0.1
            scale = round(scale,1)
            print("scale")
            if scale == 1.7:
                print("1.8")
                scale = 1.8
        else:
            scale -=0.1
            scale = round(scale,1)
            print(scale)
            if scale < 0.7:
                scale = 0.7
            elif scale == 1.7:
                print("1.6")
                scale = 1.6

        with open(
            f".{self.sep}Ui{self.sep}size_guide.qss",
            "w",
            encoding="UTF-8") as sizes:
            sizes.write(str(scale)+"\n"+stylesheet)

    def get_size_stylesheet(self) -> tuple:
        """
        Gets and formats the size style guide for the GUI.
        """

        with open(
            f".{self.sep}Ui{self.sep}size_guide.qss",
            "r",
            encoding="UTF-8") as sizes:
            scale = float(sizes.readline())
            stylesheet = sizes.read()

        stylesheet = stylesheet.replace("18", str(int(18*scale)))
        stylesheet = stylesheet.replace("24", str(int(24*scale)))
        stylesheet = stylesheet.replace("30", str(int(30*scale)))

        return stylesheet, scale
