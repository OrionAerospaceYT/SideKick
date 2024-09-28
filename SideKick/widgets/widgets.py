"""
The widgets class
"""

import time

class Widgets:
    """
    Super class to DeviceManagerWindow, FileManagerWindow, and RecordLight

    Attributes:
        show (bool): whether or not to display the GUI
        width (int): the width of the widget
        height (int): the height of the widget

    Methods:
        get_show:
            Returns:
                bool: whether or not to show the GUI
        get_height:
            Returns:
                int: the height of the widget
        get_width:
            Returns:
                int: the width of the widget
    """

    def __init__(self, state=False, width=0, height=0):
        self.show = state
        self.width = width
        self.height = height

    def update_show(self):
        """
        converts show to not show
        """
        self.show = not self.show

    def get_show(self):
        """
        Returns:
            bool: whether or not to show the GUI
        """
        return self.show

    def get_height(self):
        """
        Returns:
            int: the height of the widget
        """
        return int(self.height)

    def get_width(self):
        """
        Returns:
            int: the width of the widget
        """
        return int(self.width)

class RecordLight(Widgets):
    """
    Blinks the record light
    This class inherits Widgets

    Attributes:
        blinking (bool): wether or not the record light is meant to blink
        running (bool): while the the app is running

    Methods:
        threaded_blink:
            blinks the light every 0.5 seconds

        update_recording:
            changes the recording status

        terminate_record:
            stops the threaded loop
    """

    def __init__(self):
        super().__init__(True)

        self.blinking = False
        self.running = True

    def threaded_blink(self):
        """
        blinks the light every 0.5 seconds
        """
        while self.running:
            if self.blinking:
                self.update_show()
            else:
                self.show = True

            time.sleep(0.75)

    def update_recording(self):
        """
        changes the recording status
        """
        self.blinking = not self.blinking

    def start_recording(self):
        """
        If not already record, record.
        """
        self.blinking = True

    def end_recording(self):
        """
        If recording, stop.
        """
        self.blinking = False

    def terminate_record(self):
        """
        stops the threaded loop
        """
        self.running = False
