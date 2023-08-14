"""
The cli manager file.
"""
import subprocess
import threading
import time

ERROR_TERMS = ["Error opening sketch", "Error during build", "exit status"]

class CliManager:
    """
    Controls the flow of commands to the CLI

    Output should be continuous with previous outputs seperated with clear headers -
    Succes,
    Fail,
    Command

    Change file -> menu
    add cli manager button (full screen)
    """

    def __init__(self, path):
        self.path = path
        self.commands = {}
        self.outputs = {}
        self.running = False
        self.enabled = True

    def get_output(self):
        """
        Removes first output from the queue
        """

        try:
            key = list(self.outputs.keys())[0]
            return key, self.outputs.pop(key)
        except IndexError:
            return None, None

    def get_status(self, key="upload"):
        """
        Gets the current status of what tasks are still to be done.
        """
        for cmd in self.commands.items():
            if cmd[1] == key:
                return True
        return False

    def check_for_upload(self, compile_out:str) -> bool:
        """
        Checks whether or not to upload if the compile was a success
        or not.
        
        Args:
            compile_out (str): the output of the compile
        
        Returns:
            bool: whether or not to compile
        """
        for item in ERROR_TERMS:
            if item in compile_out:
                return False
        return True

    def threaded_call(self):
        """
        Puts the command on the thread to be non blocking
        """
        prev_output = ""

        while self.enabled:
            if not self.commands.keys():
                time.sleep(0.25)
                continue

            cmd = list(self.commands.keys()).pop(0)

            if "upload" in cmd:
                if not self.check_for_upload(prev_output):
                    self.commands.pop(cmd)
                    continue

            cmd_type = self.commands[cmd]

            self.running = True

            prev_output = self.get_cmd_output(cmd).decode("UTF-8")

            self.outputs[prev_output] = cmd_type
            self.commands.pop(cmd)

            self.running = False

    def communicate(self, cmd, cmd_type="usr"):
        """
        Calls the thread to run the command

        Args:
            cmd (string): the command to run in terminal
            cmd_type (string): what type of command
            ('usr' = user input, 'compile' = compile, 'upload' = upload)
        """
        self.commands[cmd] = cmd_type

    def get_cmd_output(self, cmd):
        """
        Runs the command in the program flow

        Args:
            cmd (string): the comand to run in terminal
        Returns:
            string: the output from CLI
        """
        with subprocess.Popen(
                    f"\"{self.path}\" {cmd}", stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True) as process:

            output = process.communicate()

        return output[0]

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
