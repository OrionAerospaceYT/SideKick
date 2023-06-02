"""
This file is responsible for handling the COM ports
and serial devices.
It uses pySerial and has a loop running on a thread.
"""

import random
import threading
import time
import subprocess
import serial
import serial.tools.list_ports
import numpy as np

MESSAGES = [b"t(Hello World)", b"t(This is working)", b"t(Not skipping data!)"]

class DeviceManager():
    """
    Handles all of the serial communications:
        Uploads
        Compiles
        Reads
        Writes
        Connect
        Disconnect
    TODO: full class docstring
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.device = None
        self.get_data = None
        self.port = None
        self.error = None

        self.connected = False
        self.auto_connect = False

        self.raw_cummulative_data = ""
        self.terminal_data = ""

        self.raw_data = []

        # private definitions
        self.__failed_recv = 0
        self.__change_in_data = []
        self.__emulated_input = b""
        self.__emulating_counter = 0
        self.__emulating = False

    def __call__(self):
        self.device = None
        self.get_data = None
        self.port = None
        self.error = None

        self.connected = False
        self.auto_connect = False

        self.raw_cummulative_data = ""
        self.terminal_data = ""

        self.raw_data = []

        # private definitions
        self.__failed_recv = 0
        self.__change_in_data = []
        self.__emulated_input = b""
        self.__emulating_counter = 0
        self.__emulating = False

    def send(self, message):
        """
        Sends the message given from the gui to the
        connected device

        Args:
            message (binary string): the message to send to the device
        """

        if self.device:
            self.device.write(f"{message}\n".encode("UTF-8"))

    def device_parse_data(self, buffer):
        """
        Parses the data buffer into self.raw_data.

        Args:
            buffer (string): the collective data
        """

        decoded_buffer = buffer.decode("UTF-8")

        if decoded_buffer.startswith("t(") or decoded_buffer.startswith("g("):
            index = 0
        else:
            index = 1

        self.raw_data.append(decoded_buffer.split("\r\n")[index])
        self.__change_in_data.append(decoded_buffer.split("\r\n")[index])
        buffer = buffer.replace(buffer.split(b"\r\n")[index] + b"\r\n", b"")

        self.raw_data = list(filter(None, self.raw_data))

        if len(self.raw_data) > 1500:
            self.raw_data.pop(0)

        return buffer

    def device_data(self):
        """
        Gets the raw data from either the emulated device or the actual
        arduino device that's connected.

        Returns:
            bytes: raw data from device
        """

        try:
            if not self.__emulating:
                raw_data = self.device.read_all()
            else:
                raw_data = self.__emulated_input
                self.__emulated_input = b""
            self.__failed_recv = 0
        except serial.SerialException:
            raw_data = ""
            self.__failed_recv += 1

        return raw_data

    def debug_device(self, raw_data):
        """
        Prints out the raw data and the data on terminal

        Args:
            raw_data (b str): the raw data through the serial port
        """
        self.raw_cummulative_data += raw_data.replace(b"\r\n", b"/n").decode("UTF-8")

        print("Raw data cummulative >>> " + self.raw_cummulative_data)

        string = ""
        for item in self.raw_data:
            string += item.replace("\r\n", "")

        print("Data on terminal >>> " + string)

    def threaded_get_raw_data(self, port, baud, dev=False):
        """
        Raw input data from the serial device
        Connects device and then while loops with no time.sleep
        Checks for "(" in the data as all sidekick messages will have one

        Args:
            port (string): the port to connect to
            baud (int): the baud rate of the connected device
        """
        self.port = port
        self.raw_cummulative_data = ""

        if not dev:
            try:
                self.device = serial.Serial(port, baud, rtscts=True)
            except serial.SerialException as error:
                self.error = str(error).replace("(","\n").replace(")","\n")
                print(self.error)
                return

        self.connected = True
        buffer = b""

        while self.connected:

            raw_data = self.device_data()

            if self.__failed_recv > 10:
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

    def terminate_device(self):
        """
        terminates the while True loop to disconnect the device
        then sets the variables back to the initial states so
        that there is no data
        """

        self.connected = False

    def connect_device(self, port="COM1", baud=115200, dev=False):
        """
        connects the device in order to read the data coming
        from the SideKick/Teensy/Arduino
        also stars the thread to get the data from the newly connected
        device

        Args:
            port (string): the com port the device is connected to e.g. "COM1"
            baud (int): the baud rate of the connected board
        """
        self()

        if dev:
            self.__emulating = True
            print("<<< WARNING >>> EMULATING DEVICE")

            emulator = threading.Thread(target=self.device_emulator)
            emulator.start()

        self.get_data = threading.Thread(target=self.threaded_get_raw_data, args=(port, baud, dev),)
        self.get_data.start()

    def scan_avaliable_ports(self, dev=False):
        """
        Gets all avaliable com ports.

        Args:
            dev (bool): whether or not to show the dev option of emulate

        Returns:
            list : avaliable com ports for pyserial
        """

        available_ports = ["emulate"] if dev else []

        for port in serial.tools.list_ports.comports():
            available_ports.append(port.device)
            #print(port.description)
            if not self.connected and ("USB" in port.description) and self.auto_connect:
                self.connect_device(str(port.device))
                time.sleep(1)
        return available_ports

    def compile_script(self, compile_cmd):
        """
        Compiles the selected script

        Args:
            compile_cmd (string): the command t ocompile the script with arduino-cli
        Returns:
            string : the error string to be parsed
        """

        compile_process = subprocess.Popen(
            compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        compile_output = compile_process.communicate()

        return compile_output[0].decode("UTF-8")

    def upload_script(self, compile_cmd, upload_cmd):
        """
        Compiles and uploads the script

        Args:
            compile_cmd (string): the command to compile the script with arduino-cli
            upload_cmd (string): the command to upload the script with arduino-cli
        Returns:
            error_output (string): the report to display on debug
            boolean: status of wether upload was success or not
        """
        upload_output = ""

        compile_process = subprocess.Popen(
            compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        compile_output = compile_process.communicate()

        compile_output = compile_output[0].decode("UTF-8")

        if "error:" not in compile_output:
            upload_process = subprocess.Popen(
                upload_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            upload_output = upload_process.communicate()
            upload_output = upload_output[0].decode("UTF-8")

        error_output = compile_output+upload_output

        return error_output

    def reset_difference(self, data):
        """
        Sets self.__change_in_data to 0 after the value
        has been used.

        Args:
            data (list): the data that is saved
        """

        self.__change_in_data = self.__change_in_data[len(data):]

    @property
    def change_in_data(self):
        """
        a getter for the private change_in_data_len attribute

        Returns:
            int: change_in_data_len
        """

        return self.__change_in_data

    def device_emulator(self):
        """
        Gives dummy inputs to dev the GUI without physical
        hardware!

        Designed to be run on a thread to emulate the device
        being disconnected from the whole system.
        """

        while self.__emulating:

            self.__emulated_input += random.choice(MESSAGES)
            self.__emulated_input += bytes(
                f"g(sin, 1, {np.sin(self.__emulating_counter * np.pi / 180)})", "UTF-8")
            if not (self.__emulating_counter - 90) % 180 == 0:
                self.__emulated_input +=  bytes(
                f"g(tan, 2, {np.tan(self.__emulating_counter * np.pi / 180)})", "UTF-8")
            self.__emulated_input += b"\r\n"

            self.__emulating_counter += 1

            time.sleep(1)
