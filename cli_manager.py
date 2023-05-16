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
        self.process = None
        self.output = None
        self.running = False

    def threaded_call(self, cmd):
        """
        Puts the command on the thread to be non blocking

        Args:
            cmd (string): the command to run in terminal
        """
        self.running = True

        self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True)

        self.output = self.process.communicate()

        self.running = False

    def communicate(self, cmd):
        """
        Calls the thread to run the command

        Args:
            cmd (string): the command to run in terminal
        """
        threading.Thread(target=self.threaded_call, args=(cmd),)
