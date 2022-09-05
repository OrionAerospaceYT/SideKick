import os
import ctypes
import sys
import pygit2
import shutil
import __main__
from datetime import datetime
import requests
import pytz
from bs4 import BeautifulSoup
import urllib

# Code for new projects
class FileManager():

    # Creates directories and files if they don't exist
    def __init__(self):
        self.file = None # Terminal Write file
        self.user = os.getlogin()
        self.cwd = os.getcwd()

        directories = os.listdir(f"C:/Users/{self.user}/Documents")
        if "SideKick" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick")

        directories = os.listdir(f"C:/Users/{self.user}/Documents/SideKick")
        if "SK Projects" not in directories:
            os.mkdir(f"C:/Users/{self.user}/Documents/SideKick/SK Projects")
        if "SavedData" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData')
        if "Libraries" not in directories:
            os.mkdir(f'C:/Users/{self.user}/Documents/SideKick/Libraries')
            src = f'./ConsciOS/libraries'
            des = f'C:/Users/{self.user}/Documents/SideKick/Libraries'
            shutil.copytree(source, destination)

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def check_for_updates(self):
        cwd = os.getcwd()

        # Gets the ConsciOS repo
        response = requests.get(url = 'https://google.com').text

        for lines in response.split("\n"):
            print("New Line", lines)

        # Gets the time the file was last edited which is the last time the file was downloaded
        last_download = str(datetime.fromtimestamp(os.path.getmtime(f"{cwd}\Externals\ConsciOS"))).split(".")[0]
        string_format = "%Y-%m-%d %H:%M:%S"

        last_download_local = datetime.strptime(last_download, string_format)
        last_download = str(last_download_local.astimezone(pytz.UTC)).split("+")[0]

        #print(last_download, last_repo_commit)
        return False #max([last_download, last_repo_commit]) == last_repo_commit

    def update(self):
        if self.is_admin():
            cwd = os.getcwd()
            os.remove(f"{cwd}\Externals\ConsciOS")
            pygit2.clone_repository("https://github.com/OrionAerospaceYT/ConsciOS/", f"{cwd}\Externals\ConsciOS")
            print("Getting latest")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            cwd = os.getcwd()
            os.remove(f"{cwd}\Externals\ConsciOS")
            pygit2.clone_repository("https://github.com/OrionAerospaceYT/ConsciOS/", f"{cwd}\Externals\ConsciOS")
            print("Getting latest")

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
        print("Continuing anyway")

        source  = f'./ConsciOS/Source'
        destination = f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}'
        shutil.copytree(source, destination)

        os.rename(f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/PROJECT.ino', f'C:/Users/{self.user}/Documents/SideKick/SK Projects/{name}/{name}.ino')

    # Starts a new save file, should be called each time a new device is connected
    def start_new_save(self):
        num_of_saves = len(os.listdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData'))
        self.file = open(f"C:/Users/{self.user}/Documents/SideKick/SavedData/Save{num_of_saves + 1}", 'w+') # The + 1 is so that it starts at 1 rather than 0

    # Saves data to file for users to read later
    def save_terminal_data(self, data):
        num_of_saves = len(os.listdir(f'C:/Users/{self.user}/Documents/SideKick/SavedData'))
        self.file.write(f'{data}\n')
