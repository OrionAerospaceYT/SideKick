import subprocess
import threading

class cli_manager:
    """
    Controls the flow of commands to the CLI
    """
    def __init__(self, path):
        self.path = path
        self.process = None
        self.output = None
        self.running = False

    def threaded_call(self, cmd):
        self.running = True

        self.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True)

        self.output = self.process.communicate()

        self.running = False

    def communicate(self, cmd):
        threading.Thread(target=self.threaded_call, args=(cmd),)