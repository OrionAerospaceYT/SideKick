"""
License
"""
import threading

import serial


class DeviceManager():
    """
    the class for dealing with getting data from
    COM ports for the main backend
    """

    def __init__(self):
        self.device = None
        self.get_data = None
        self.raw_data = ""

        self.terminal_data = ""
        self.graph_top_data = []
        self.graph_bottom_data = []

    def threaded_get_raw_data(self, port, baud):
        """
        this function runs on a thread and only gets the
        raw input data from the com port as a binary string
        if the device is connected
        """

        self.device = serial.Serial(port, baud, timeout=0, rtscts=False)
        while self.device is not None:
            raw_data = self.device.readline().decode("utf-8")
            if "\n" in raw_data:
                self.raw_data = raw_data

    def decode_graph_data(self):
        """
        parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        to graph_top_data, graph_bottom_data which are lists
        example graph output would be: [[1,2,3,4,5,],[5,4,3,2,1],[2,5,4,1,3]]

        this data still needs to be processed as it is in string form
        the processing will go in the main backend
        """

        raw_list = self.raw_data.split("g(")

        for data in raw_list:
            data = data.split(")")
            if "t(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                valid_graph_data = data[0].replace(" ", "").split(",")
                if valid_graph_data[1] == "1":
                    self.graph_top_data.append(valid_graph_data[2])
                else:
                    self.graph_bottom_data.append(valid_graph_data[2])

        return self.graph_top_data, self.graph_bottom_data

    def decode_terminal_data(self):
        """
        parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        to terminal_data which is a string
        all terminal data from one output is put into a single line
        """

        raw_list = self.raw_data.split("t(")
        self.terminal_data = ""

        for data in raw_list:
            data = data.split(")")
            if "g(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                self.terminal_data += " " + data[0]

        return self.terminal_data

    def terminate_device(self):
        """
        terminates the while True loop to disconnect the device
        then sets the variables back to the initial states so
        that there is no data
        """

        self.device = None
        self.raw_data = ""

        self.terminal_data = ""
        self.graph_top_data = []
        self.graph_bottom_data = []

    def connect_device(self, port="COM1", baud=115200):
        """
        connects the device in order to read the data coming
        from the SideKick/Teensy/Arduino
        also stars the thread to get the data from the newly connected
        device
        """

        self.get_data = threading.Thread(
            target=self.threaded_get_raw_data, args=(port, baud),)
        self.get_data.start()


# only runs if this is the file being run
# the unit test will go here
if __name__ == "__main__":

    deviceManager = DeviceManager()

    deviceManager.terminate_device()

    deviceManager.raw_data = "g(name,1,1)t(text)g(name,1,2)t(text)g(name,2,3)t(text)"

    # checks the terminal output
    EXPECTED = ' text text text'
    output = deviceManager.decode_terminal_data()

    if output == EXPECTED:
        print("TEST 1: PASS")
    else:
        print(f"TEST 1: FAIL - Got ({output}) when expecting ({EXPECTED})!")

    # checks grpah output
    EXPECTED = (["1", "2"], ["3"])
    output = deviceManager.decode_graph_data()

    if output == EXPECTED:
        print("TEST 2: PASS")
    else:
        print(f"TEST 2: FAIL - Got ({output}) when expecting ({EXPECTED})!")
