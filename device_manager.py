"""
This file is responsible for handling the COM ports
and serial devices.
It uses pySerial and has a loop running on a thread.
"""


# import random

import threading
import time

#import numpy as np

import serial
import serial.tools.list_ports

from globals import TERMINAL_BEGINNING, TERMINAL_ENDING
from globals import GRAPH_BEGINNING, START_REC, END_REC


class DeviceManager():
    """
    Handles all of the serial communications:
        Uploads
        Compiles
        Reads
        Writes
        Connect
        Disconnect

    Attributes:
        parent (MainGUI) : the main gui the app is running off of
        device (Serial) : the serial device the app connects to
        port (str) : the port the device is currently connected to
        last_port (str) : the port the device was connected to
        error (str) : the error if there was an error connecting
        target (str) : the device to auto connect to
        connected (bool) : wether or not a device is connected
        auto_connect (bool) : wether the GUI should try to auto connect if there is a port
        raw_cummulative_data (str) : the raw data from the gui that is continually added
        raw_data (list) : the data split into lines

    Methods:
        send:
            Sends the message given from the gui to the
            connected device

        device_parse_data:
            Parses the data buffer into self.raw_data

        device_data:
            Gets the raw data from either the emulated device or the actual
            arduino device that's connected

        debug_device:
            Prints out the raw data and the data on terminal

        threaded_get_raw_data:
            Raw input data from the serial device
            Connects device and then while loops with no time.sleep
            Checks for "(" in the data as all sidekick messages will have one

        terminate_device:
            Terminates the while True loop to disconnect the device
            then sets the variables back to the initial states so
            that there is no data

        connect_device:
            Connects the device in order to read the data coming
            from the SideKick/Teensy/Arduino
            also stars the thread to get the data from the newly connected
            device

        scan_avaliable_ports:
            Gets all avaliable com ports and auto connects to devices

        reset_difference:
            Sets self.change_in_data to 0 after the value has been used.

        device_emulator:
            Gives dummy inputs to dev the GUI without physical hardware!
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.device = None
        self.port = None
        self.last_port = None
        self.error = None
        self.target = None

        self.connected = False
        self.auto_connect = False

        self.raw_cummulative_data = ""

        self.raw_data = []

        self.failed_recv = 0
        self.change_in_data = []
        self.emulated_input = b""
        self.emulating_counter = 0
        self.emulating = False

        self.start_rec = False
        self.end_rec = False

    def __call__(self):
        self.device = None
        self.port = None
        self.error = None
        self.target = None

        self.connected = False
        self.auto_connect = True

        self.raw_cummulative_data = ""

        self.raw_data = []

        # private definitions
        self.failed_recv = 0
        self.change_in_data = []
        self.emulated_input = b""
        self.emulating_counter = 0
        self.emulating = False

    def send(self, message:str):
        """
        Sends the message given from the gui to the
        connected device

        Args:
            message (str): the message to send to the device
        """

        if self.device:
            self.device.write(f"{message}\n".encode("UTF-8"))

    def device_parse_data(self, buffer:str) -> str:
        """
        Parses the data buffer into self.raw_data

        Args:
            buffer (str): the collective data
        
        Returns:
            str: the buffer of incomplete mesages
        """
        try:
            decoded_buffer = buffer.decode("UTF-8")
        except UnicodeDecodeError:
            decoded_buffer = TERMINAL_BEGINNING + "ERROR" + TERMINAL_ENDING

        terminal_beginning = decoded_buffer.startswith(TERMINAL_BEGINNING)
        graph_beginning = decoded_buffer.startswith(GRAPH_BEGINNING)

        if terminal_beginning or graph_beginning:
            index = 0
        else:
            index = 1

        self.raw_data.append(decoded_buffer.split("\r\n")[index])
        buffer = buffer.replace(buffer.split(b"\r\n")[index] + b"\r\n", b"")

        if START_REC.encode("UTF-8") in buffer:
            self.start_rec = True
        elif END_REC.encode("UTF-8") in buffer:
            self.end_rec = True

        buffer = buffer.replace(START_REC.encode("UTF-8"), b"")
        buffer = buffer.replace(END_REC.encode("UTF-8"), b"")

        self.raw_data = list(filter(None, self.raw_data))

        return buffer

    def device_data(self) -> str:
        """
        Gets the raw data from either the emulated device or the actual
        arduino device that's connected

        Returns:
            str: raw data from device
        """

        try:
            if not self.emulating:
                raw_data = self.device.read_all()
            else:
                raw_data = self.emulated_input
                self.emulated_input = b""
            self.failed_recv = 0
        except serial.SerialException:
            raw_data = ""
            self.failed_recv += 1

        return raw_data

    def debug_device(self, raw_data:str):
        """
        Prints out the raw data and the data on terminal

        Args:
            raw_data (str): the raw data through the serial port
        """
        self.raw_cummulative_data += raw_data.replace(b"\r\n", b"/n").decode("UTF-8")

        print("Raw data cummulative >>> " + self.raw_cummulative_data)

        string = ""
        for item in self.raw_data:
            string += item.replace("\r\n", "")

        print("Data on terminal >>> " + string)

    def threaded_get_raw_data(self, port:str, baud:int, dev=False):
        """
        Raw input data from the serial device
        Connects device and then while loops with no time.sleep
        Checks for "(" in the data as all sidekick messages will have one

        Args:
            port (string): the port to connect to
            baud (int): the baud rate of the connected device
            dev (bool): whether the app is emulating or not
        """
        self.port = port
        self.raw_cummulative_data = ""

        if not dev:
            try:
                self.device = serial.Serial(port, baud, rtscts=True)
                #initial_data = b""
                #while not initial_data:
                #    initial_data = self.device_data()
            except serial.SerialException as error:
                self.error = str(error).replace("(","\n").replace(")","\n")
                print("<<< ERROR >>> " + self.error)
                return

        self.connected = True
        buffer = b""

        while self.connected:

            raw_data = self.device_data()

            if self.failed_recv > 10:
                break

            if not (raw_data != b"" and isinstance(raw_data, bytes)):
                continue

            buffer += raw_data
            buffer = buffer.replace(b"\r\n\r\n", b"\r\n")

            if buffer.startswith(b"\r\n"):
                buffer = buffer[2:]

            while buffer.count(b"\r\n") > 1 or buffer.endswith(b"\r\n"):
                buffer = self.device_parse_data(buffer)

        if self.device:
            self.device.close()

        self()
        self.target = self.last_port
        self.auto_connect = False

    def terminate_device(self):
        """
        Terminates the while True loop to disconnect the device
        then sets the variables back to the initial states so
        that there is no data.
        """

        while self.connected:
            self.connected = False
            self.last_port = self.port
            time.sleep(0.2)

    def connect_device(self, port="COM1", baud=115200, dev=False):
        """
        Connects the device in order to read the data coming
        from the SideKick/Teensy/Arduino
        also stars the thread to get the data from the newly connected
        device

        Args:
            port (string): the com port the device is connected to e.g. "COM1"
            baud (int): the baud rate of the connected board
            dev (bool): emulates a device if the user wants
        """
        self()

        if dev:
            self.emulating = True
            print("<<< WARNING >>> EMULATING DEVICE")
            emulator = threading.Thread(target=self.device_emulator)
            emulator.start()
        else:
            self.auto_connect = True
            self.target = port

        get_data = threading.Thread(
            target=self.threaded_get_raw_data, args=(port, baud, dev),)
        get_data.start()

    def scan_avaliable_ports(self, dev=False) -> list:
        """
        Gets all avaliable com ports and auto connects to devices.

        Args:
            dev (bool): whether or not to show the dev option of emulate

        Returns:
            list : avaliable com ports for pyserial
        """

        available_ports = ["emulate"] if dev else []

        for port in serial.tools.list_ports.comports():
            available_ports.append(port.device)

        # Auto connection
        if not self.connected and self.auto_connect:
            if self.target is not None and (self.target in available_ports):
                self.connect_device(self.target)
                time.sleep(1)

        return available_ports

    def reset_difference(self, data:list):
        """
        Sets self.change_in_data to 0 after the value
        has been used.

        Args:
            data (list): the data that is saved
        """

        self.change_in_data = self.change_in_data[len(data):]

    def device_emulator(self):
        """
        Gives dummy inputs to dev the GUI without physical
        hardware!

        Designed to be run on a thread to emulate the device
        being disconnected from the whole system.
        """

        while self.emulating:

            # self.emulated_input += random.choice(MESSAGES)
            #self.emulated_input += bytes(f"t({self.emulating_counter})", "UTF-8")
            #self.emulated_input += bytes(
            #    f"g(sin, 1, {np.sin(self.emulating_counter * np.pi / 180)})", "UTF-8")

            #self.emulated_input +=  bytes(
            #    f"g(cos, 1, {np.cos(self.emulating_counter * np.pi / 180)})", "UTF-8")
            #self.emulated_input += b"\r\n
            self.emulated_input += bytes(
                f"{TERMINAL_BEGINNING}{self.emulating_counter}{TERMINAL_ENDING}\r\n", "UTF-8")

            self.emulating_counter += 1

            time.sleep(0.5)
