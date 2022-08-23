import os
import shutil
import __main__

# Code for new projects
class FileManager():

    # Creates directories and files if they don't exist
    def __init__(self):
        self.file = None # Terminal Write file
        self.user = os.getlogin()

        directories = os.listdir(f"C:/Users/{self.user}/Documents")
        if "SideKick" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick")

        directories = os.listdir(f"C:/Users/{self.user}/Documents/SideKick")
        if "SK Projects" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        if "SavedData" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData')

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
        projects = os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        return projects

    # Adds new projects when "new project"
    def add_new_project(self, name):
        if name in os.listdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects"):
            return 0 # Used for error handling, if this is returned red html is displayed
        source  = f'./ConsciOS/Source'
        destination = f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}'
        shutil.copytree(source, destination)
        lib_source = f'./ConsciOS/Libraries'
        lib_destination = f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/Libraries'
        shutil.copytree(lib_source, lib_destination)
        os.rename(f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/PROJECT.ino', f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/{name}.ino')
        return 1

    # Starts a new save file, should be called each time a new device is connected
    def start_new_save(self):
        num_of_saves = len(os.listdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData'))
        self.file = open(f"C:/Users/{self.user}/Documents/SideKick/SavedData/Save{num_of_saves + 1}", 'w+') # The + 1 is so that it starts at 1 rather than 0

    # Saves data to file for users to read later
    def save_terminal_data(self, data):
        num_of_saves = len(os.listdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData'))
        self.file.write(f'{data}\n')
