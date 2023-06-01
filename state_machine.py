"""
A python state machine for the sidekick app.
"""

import time
import threading
from cli_manager import CliManager

class StateMachine():
    """
    A python state machine for the sidekick app.
    """

    def __init__(self, cli_path):

        self.debug_window = False
        self.showing_data = False

        self.cli_status = False
        self.cli_manager = CliManager(cli_path)

    def dummy_delay(self, delay):
        """
        A test function to simulate a delay.

        Args:
            delay (int): the delay
        """
        time.sleep(delay)

    def set_cli_status(self, cmd):
        """
        TODO

        Args:
            cmd (string): the command to run on the arduino cli
        """
        my_thread = threading.Thread(target=self.dummy_delay, args=(10,),)
        my_thread.start()

    def set_debug_window(self, debug_window):
        """
        Sets the value of self.debug_window

        Args:
            debug_window (boolean): the new value of self.debug_window
        """
        self.debug_window = debug_window

    def status_checker(self):
        """
        Checks all status' of ongoing tasks and this function is to be run on a thread.
        """
        pass
