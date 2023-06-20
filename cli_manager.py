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
        print(self.commands)
        for cmd in self.commands.items():
            print(cmd)
            if cmd[1] == key:
                return True
        return False

    def threaded_call(self):
        """
        Puts the command on the thread to be non blocking
        """

        while self.enabled:
            if not self.commands.keys():
                time.sleep(0.25)
                continue

            cmd =  list(self.commands.keys()).pop(0)
            cmd_type = self.commands[cmd]

            self.running = True
            with subprocess.Popen(
                    cmd, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True) as process:
                output = process.communicate()

            self.outputs[output[0].decode("UTF-8")] = cmd_type
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
        self.commands[f"\"{self.path}\" {cmd}"] = cmd_type

    def get_cmd_output(self, cmd):
        """
        Runs the command in the program flow

        Args:
            cmd (string): the comand to run in terminal
        Returns:
            string: the output from CLI
        """
        print(f"\"{self.path}\" {cmd}")
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
