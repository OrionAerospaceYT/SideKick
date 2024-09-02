"""
The save manager is used to record and export data saved from the device that is using the
SideKick GUI.
"""

import os
import re

from PyQt6 import QtWidgets as qtw

from SideKick.globals import GRAPH_BEGINNING, GRAPH_ENDING

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
