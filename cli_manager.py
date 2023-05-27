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
        self.cmd = None
        self.process = None
        self.output = None
        self.running = False

    def threaded_call(self):
        """
        Puts the command on the thread to be non blocking

        Args:
            cmd (string): the command to run in terminal
        """
        self.running = True

        self.process = subprocess.Popen(
                self.cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True)

        self.output = self.process.communicate()
        print(self.output[0])
        self.cmd = None
        self.running = False

    def communicate(self, cmd):
        """
        Calls the thread to run the command

        Args:
            cmd (string): the command to run in terminal
        """
        if self.cmd is not None:
            self.process.kill()
            print(f"<<< WARNING >>> KILLED PROCESS: {self.cmd}")

        self.cmd = cmd
        call = threading.Thread(target=self.threaded_call, args=(),)
        call.start()

if __name__ == "__main__":

    PATH = "\"./Externals/arduino-cli-windows.exe\""

    cli = CliManager(PATH)

    while True:

        command = input(">>> ")

        if command.lower() == "exit":
            break

        else:
            cli.communicate(PATH + " " + command)
