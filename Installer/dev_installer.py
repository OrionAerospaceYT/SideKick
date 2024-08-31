"""
This installs and organises all of the files needed for
development mode
"""

import os
import platform

def change_user():
    """
    Uses the template in this directory to update
    the "Arduino15" files
    """

    print("<<< RUNNING >>> Updating the sidekick config")

    with open(f".{SEP}cli_yaml_example.yaml", "r", encoding="UTF-8") as yaml:
        yaml_file = yaml.read()

    downloads = ARDUINO + "staging"
    libraries = DOCUMENTS + "SideKick" + SEP + "Libraries"

    directories = f"directories:\n\
    data: {ARDUINO}\n\
    downloads: {downloads}\n\
    user: {libraries}"

    yaml_file = yaml_file.replace("directories:", directories)

    with open(f"{ARDUINO}{SEP}arduino-cli.yaml", "w", encoding="UTF-8") as yaml:
        yaml.write(yaml_file)

def install_boards():
    """
    Installs all of the key boards such as:
    Raspberry PI Pico
    Arduino Uno, nano, etc..
    Teensy 4.1, 4.0, 3.6, etc...
    """

    print("<<< RUNNING >>> Installing your boards")

    os.system(CLI + " core install arduino:avr")
    os.system(CLI + " core install teensy:avr")
    os.system(CLI + " core install arduino:mbed_rp2040")

def install_requirements():
    """
    Installs all pip requirements for python that are
    listed in the "requirements.txt" file
    """

    print("<<< RUNNING >>> Installing pip requirements")

    requirements_path = f"..{SEP}requirements.txt"
    os.system(f"pip install -r {requirements_path}")

def sidekick_shortcut():
    """
    Creates a shortcut to the desktop.
    """

    if OPERATING_SYSTEM == "Windows":
        os.system("pip install pyinstaller")
        os.system("pyinstaller --onefile --icon=\"../Ui/SideKick.ico\" ../main.py")


if __name__ == "__main__":

    print("Welcome to the SideKick development mode installer!\n")
    print("This is the installer which will allow easy development of")
    print("the SideKick App.\n")
    print("<<< WARNING >>> This installer will edit the arduino files")
    print("and add the following directories to Documents:")
    print("    SideKick\n")
    print("This will also create a desktop shortcut .bat/.sh file to")
    print("run the SideKick App.\n")

    while True:
        answer = input("Would you like to proceed? (Y/N): ")
        if answer.lower() in ("y", "yes"):
            break
        elif answer.lower() in ("n", "no"):
            exit()
        else:
            print("<<< ERROR >>> Invalid input, please answer Y or N")

    OPERATING_SYSTEM = platform.system()
    USER = os.getlogin()

    if OPERATING_SYSTEM == "Windows":
        SEP = "\\"
        CLI = "..\\Externals\\arduino-cli-windows.exe"
        DOCUMENTS = f"C:\\Users\\{USER}\\Documents\\"
        ARDUINO = f"C:\\Users\\{USER}\\AppData\\Local\\Arduino15\\"
        TYPE = ".bat"

    elif OPERATING_SYSTEM == "Darwin":
        SEP = "/"
        CLI = "../Externals/arduino-cli-mac"
        DOCUMENTS = f"/Users/{USER}/documents/"
        ARDUINO = f"/Users/{USER}/Library/Arduino15//"
        TYPE = ".sh"

    elif OPERATING_SYSTEM == "Linux":
        SEP = "/"
        CLI = "../Externals/arduino-cli-linux.sh"
        DOCUMENTS = f"/home/{USER}/Documents/"
        ARDUINO = f"/home/{USER}/.arduino15/"
        TYPE = ".sh"

    else:
        print(f"<<< ERROR >>> OS {OPERATING_SYSTEM} is not yet supported")
        exit()

    os.system(CLI + " config init")
    change_user()
    install_boards()
    install_requirements()
    sidekick_shortcut()
