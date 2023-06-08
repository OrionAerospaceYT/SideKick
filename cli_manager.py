"""
The cli manager file.
"""
import subprocess
import threading
import time

class CliManager:
    """
    Controls the flow of commands to the CLI

    TODO:
    keep as is, add fullscreen that removes graphs + terminal

    Output should be continuous with previous outputs seperated with clear headers -
    Succes,
    Fail,
    Command

    Change file -> menu
    add cli manager button (full screen)
    """

    def __init__(self, path):
        self.path = path
        self.commands = []
        self.outputs = []
        self.running = False
        self.enabled = True

    def get_output(self):
        """
        Removes first output from the queue
        """
        try:
            return self.outputs.pop(0)
        except IndexError:
            return None

    def threaded_call(self):
        """
        Puts the command on the thread to be non blocking
        """

        while self.enabled:
            if not self.commands:
                time.sleep(0.25)
                continue

            self.running = True
            with subprocess.Popen(
                    self.commands.pop(0), stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True) as process:
                output = process.communicate()

            self.outputs.append(output[0].decode("UTF-8"))

            self.running = False

    def communicate(self, cmd):
        """
        Calls the thread to run the command

        Args:
            cmd (string): the command to run in terminal
        """
        self.commands.append(f"\"{self.path}\" {cmd}")

    def terminate(self):
        """
        Ends the threaded function if it is running.
        """
        self.enabled = False


if __name__ == "__main__":

    PATH = "./Externals/arduino-cli-windows.exe"

    cli = CliManager(PATH)

    command_runner = threading.Thread(target=cli.threaded_call, args=(),)
    command_runner.start()

    while True:

        command = input(">>> ")

        if command.lower() == "exit":
            break

        cli.communicate(command)

    cli.terminate()
