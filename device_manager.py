"""
This file is responsible for handling the COM ports
and serial devices.
It uses pySerial and has a loop running on a thread.
"""

import glob
import sys
import threading
import subprocess
import serial


class DeviceManager():
    """
    Handles all of the serial communications:
        Uploads
        Compiles
        Reads
        Writes
        Connect
        Disconnect
    """

    def __init__(self):
        self.device = None
        self.get_data = None
        self.port = None
        self.error = None

        self.failed_recv = 0

        self.connected = False

        self.raw_cummulative_data = ""
        self.terminal_data = ""

        self.raw_data = []

    def __call__(self):
        self.device = None
        self.get_data = None
        self.port = None
        self.error = None

        self.failed_recv = 0

        self.connected = False

        self.raw_cummulative_data = ""
        self.terminal_data = ""

        self.raw_data = []

    def send(self, message):
        """
        Sends the message given from the gui to the
        connected device

        Args:
            message (binary string): the message to send to the device
        """

        self.device.write(message.encode("UTF-8"))

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

    def threaded_get_raw_data(self, port, baud):
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

        try:
            self.device = serial.Serial(port, baud, rtscts=True)
            self.connected = True
        except serial.SerialException as error:
            self.error = error
            return

        buffer = b""

        while self.connected:
            try:
                raw_data = self.device.read_all()
                self.failed_recv = 0
            except serial.SerialException:
                raw_data = ""
                self.failed_recv += 1
                if self.failed_recv == 10:
                    self.terminate_device()
                    break

            if raw_data != b"":
                buffer += raw_data
                buffer = buffer.replace(b"\r\n\r\n", b"\r\n")
                if buffer.startswith(b"\r\n"):
                    buffer = buffer[2:]

                while buffer.count(b"\r\n") > 1 or buffer.endswith(b"\r\n"):

                    decoded_buffer = buffer.decode("UTF-8")

                    index = None
                    if decoded_buffer.startswith("t(") or decoded_buffer.startswith("g("):
                        index = 0
                    else:
                        index = 1

                    if index is not None:
                        self.raw_data.append(decoded_buffer.split("\r\n")[index])
                        buffer = buffer.replace(buffer.split(b"\r\n")[index] + b"\r\n", b"")

                    self.raw_data = list(filter(None, self.raw_data))

                    if len(self.raw_data) > 1500:
                        self.raw_data.pop(0)

        if self.device is not None:
            self.device.close()

        self()

    def terminate_device(self):
        """
        terminates the while True loop to disconnect the device
        then sets the variables back to the initial states so
        that there is no data
        """

        self.connected = False

    def connect_device(self, port="COM1", baud=115200):
        """
        connects the device in order to read the data coming
        from the SideKick/Teensy/Arduino
        also stars the thread to get the data from the newly connected
        device

        Args:
            port (string): the com port the device is connected to e.g. "COM1"
            baud (int): the baud rate of the connected board
        """

        self.get_data = threading.Thread(target=self.threaded_get_raw_data, args=(port, baud),)
        self.get_data.start()

    def scan_avaliable_ports(self, port):
        """
        iterates through each com port and checks if it can be opened or not

        https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

        Args:
            port (string): the current com port connected to the gui

        Returns:
            result (list): avaliable com ports for pyserial
        """

        if sys.platform.startswith("win"):
            ports = [f"COM{i}" for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            ports = glob.glob("/dev/tty*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")

        result = []
        if port is not None:
            result.append(port)

        for sys_port in ports:
            try:
                serial_port = serial.Serial(sys_port)
                serial_port.close()
                result.append(sys_port)
            except (OSError, serial.SerialException):
                pass

        return result

    def compile_script(self, compile_cmd):
        """
        Compiles the selected script

        Args:
            compile_cmd (string): the command t ocompile the script with arduino-cli
        Returns:
            compile_output[0] (string): the error string to be parsed
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
