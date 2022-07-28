import os
import shutil
import __main__

# Code for new projects
class FileManager():

    # Creates directories and files if they don't exist
    def __init__(self):
        self.file = None # Terminal Write file

        directories = os.listdir(os.getcwd())
        if "Projects" not in directories:
            os.mkdir(f'./Projects')

        if "SavedData" not in directories:
            os.mkdir(f'./SavedData')

    # Returns dictionary of devices
    def get_all_boards(self):
        board_dict = {}
        with open("./Ui/boards.csv","r") as boards:
            for line in boards:
                names = line.split(", ")
                board_dict[names[0]] = names[1].strip()

        return board_dict

    # Returns all project directories except for Libraries
    def get_all_projects(self):
        projects = os.listdir(f'./Projects')
        return projects

    # Adds new projects when "new project"
    def add_new_project(self, name):
        if name in os.listdir(f'./Projects'):
            return 0 # Used for error handling, if this is returned red html is displayed
        source  = f'./ConsciOSs/Source'
        destination = f'./Projects/{name}'
        shutil.copytree(source, destination)
        lib_source = f'./ConsciOSs/Libraries'
        lib_destination = f'./Projects/{name}/Libraries'
        shutil.copytree(lib_source, lib_destination)
        os.rename(f'./Projects/{name}/PROJECT.ino', f'./Projects/{name}/{name}.ino')
        return 1

    # Starts a new save file, should be called each time a new device is connected
    def start_new_save(self):
        num_of_saves = len(os.listdir(f'./SavedData'))
        self.file = open(f'./SavedData/Save{num_of_saves + 1}', 'w+') # The + 1 is so that it starts at 1 rather than 0

    # Saves data to file for users to read later
    def save_terminal_data(self, data):
        num_of_saves = len(os.listdir(f'./SavedData'))
        self.file.write(f'{data}\n')
