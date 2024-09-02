"""
Loads information about libraries and board packages for the use within the GUI
"""
import os
import json

from deepmerge import always_merger

from SideKick.file_manager.html_generator import HtmlGenerator

class JsonLibraryManager(HtmlGenerator):
    """
    Json loader class that gets all information for the arduino
    library manager.
    """

    def __init__(self, path):

        self.lib_path = path
        self.libraries = {}
        self.load_libs()

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
    def __init__(self, path, start, end):

        self.arduino_path = path
        self.packages_paths = self.get_paths(start, end)
        self.boards = {}
        self.load_boards()

    def get_paths(self, start, end):
        """
        Gets all the packages including the non arduino packages from the
        arduino15 folder.
        """
        files = []
        for packages in os.listdir(self.arduino_path):
            if packages.startswith(start) and packages.endswith(end):
                files.append(self.arduino_path + packages)
        return files

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

    def merge_json_files(self):
        """
        As there will be external packages for the arduino library - the contents of all
        of the packages indeces need to be merged
        """
        final_result = {}
        for package in self.packages_paths:
            with open(package, 'r', encoding="UTF-8") as content:
                data = json.load(content)
                final_result = always_merger.merge(final_result, data)
        return final_result

    def load_boards(self):
        """
        Loads all libraries from the library.json file in arduino15.
        """
        package_dict = self.merge_json_files()

        print(package_dict.keys())
        packages = package_dict.get("packages")

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
