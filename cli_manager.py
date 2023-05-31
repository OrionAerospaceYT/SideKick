"""
The cli manager file.
"""
import subprocess
import threading

class CliManager:
    """
    Controls the flow of commands to the CLI
    """

    def __init__(self, path):
        self.path = path
        self.thread = None
        self.output = None
        self.running = False
        self.process = None

    def threaded_call(self, cmd):
        """
        Puts the command on the thread to be non blocking

        Args:
            cmd (string): the command to run in terminal
        """

        self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True)
        self.output = self.process.communicate()

        if self.running:

            print("DONE\n>>> ",end="")

        self.running = False

    def communicate(self, cmd):
        """
        Calls the thread to run the command

        Args:
            cmd (string): the command to run in terminal
        """
        if self.running:
            print("<<< WARNING >>> KILLING PROCESS")
            self.running = False
            self.thread.join()

        self.running = True
        self.thread = threading.Thread(target=self.threaded_call, args=(cmd,),)
        self.thread.start()

if __name__ == "__main__":

    PATH = "\"./Externals/arduino-cli-windows.exe\""

    cli = CliManager(PATH)

    while True:

        command = input(">>> ")

        if command.lower() == "exit":
            break

        else:
            cli.communicate(PATH + " " + command)
