import os
import platform

class SideKickInstaller():
    """
    This class holds the functions and terminal calls required to install the SideKick GUI
    with all of its functions.
    """
    def __init__(self):
        print("<<< STARTING >>> Initialising installer")

        self.os = platform.system()
        self.user = os.getenv("USER") or os.getenv("USERNAME")

        if self.os == "Windows":
            self.sep = "\\"
            self.cli = "..\\Externals\\arduino-cli-windows.exe"
            self.documents = f"C:\\Users\\{self.user}\\Documents\\"
            self.arduino = f"C:\\Users\\{self.user}\\AppData\\Local\\Arduino15\\"
            self.type = ".bat"

        elif self.os == "Darwin":
            self.sep = "/"
            self.cli = "../Externals/arduino-cli-mac"
            self.documents = f"/Users/{self.user}/documents/"
            self.arduino = f"/Users/{self.user}/Library/Arduino15//"
            self.type = ".sh"

        elif self.os == "Linux":
            self.sep = "/"
            self.cli = "../Externals/arduino-cli-linux.sh"
            self.documents = f"/home/{self.user}/Documents/"
            self.arduino = f"/home/{self.user}/.arduino15/"
            self.type = ".sh"

        else:
            print(f"<<< ERROR >>> OS {self.os} is not yet supported")
            exit()

        os.system(self.cli + " config init")

    def change_user_yaml(self):
        """
        Uses the template in this directory to update
        the "Arduino15" files
        """
        print("<<< RUNNING >>> Updating the sidekick config")

        with open(f".{self.sep}cli_yaml_example.yaml", "r", encoding="UTF-8") as yaml:
            yaml_file = yaml.read()

        downloads = self.arduino + "staging"
        libraries = self.documents + "SideKick" + self.sep + "Libraries"

        directories = f"directories:\n\
        data: {self.arduino }\n\
        downloads: {downloads}\n\
        user: {libraries}"

        yaml_file = yaml_file.replace("directories:", directories)

        with open(f"{self.arduino }{self.sep}arduino-cli.yaml", "w", encoding="UTF-8") as yaml:
            yaml.write(yaml_file)

    def install_boards(self):
        """
        Installs all of the key boards such as:
        Raspberry PI Pico
        Arduino Uno, nano, etc..
        Teensy 4.1, 4.0, 3.6, etc...
        """
        print("<<< RUNNING >>> Installing your boards")

        os.system(self.cli + " core install arduino:avr")
        os.system(self.cli + " core install teensy:avr")
        os.system(self.cli + " core install arduino:mbed_rp2040")

    def setup_folders(self):
        """
        TODO
        """
        pass

def install():
    """
    Run the installer in the correct order.
    """
    installer = SideKickInstaller()
    installer.change_user_yaml()
    installer.install_boards()
    installer.setup_folders()

if __name__ == "__main__":
    install()
