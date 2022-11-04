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
    the class for dealing with getting data from
    COM ports for the main backend
    """

    def __init__(self):
        self.device = None
        self.get_data = None
        self.port = None
        self.raw_data = []

        self.terminal_data = ""
        self.graph_top_data = []
        self.graph_bottom_data = []

    def send(self, message):
        """
        sends the message given from the gui to the
        connected device

        Args:
            message (binary string): the message to send to the device
        """

        self.device.write(message.encode("UTF-8"))

    def threaded_get_raw_data(self, port, baud):
        """
        this function runs on a thread and only gets the
        raw input data from the com port as a binary string
        if the device is connected

        Args:
            port (string): the port to connect to
            baud (int): the baud rate of the connected device
        """

        self.port = port
        self.terminate_device()

        try:
            self.device = serial.Serial(port, baud, timeout=0, rtscts=False)
        except serial.SerialException:
            self.device = None

        while self.device is not None:

            try:
                raw_data = self.device.readline().decode("utf-8")
            except serial.SerialException:
                self.terminate_device()
                break

            # uses "(" as a bracket is in every message
            if "(" in raw_data:
                self.raw_data.append(raw_data.strip())

                if len(self.raw_data) > 1000:
                    self.raw_data.pop(0)

        self.port = None

    def terminate_device(self):
        """
        terminates the while True loop to disconnect the device
        then sets the variables back to the initial states so
        that there is no data
        """

        self.device = None
        self.raw_data = []

        self.terminal_data = ""
        self.graph_top_data = []
        self.graph_bottom_data = []

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

        self.get_data = threading.Thread(
            target=self.threaded_get_raw_data, args=(port, baud),)
        self.get_data.start()

    def scan_avaliable_ports(self):
        """
        iterates through each com port and checks if it can be opened or not

        https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

        Returns:
            list: avaliable com ports for pyserial
        """

        if sys.platform.startswith('win'):
            ports = [f'COM{i}' for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = ["Select COM"]
        for port in ports:
            try:
                serial_port = serial.Serial(port)
                serial_port.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result

    def upload_script(self, compile_cmd, upload_cmd):
        """
        Compiles and uploads the script

        Args:
            compile_cmd (string): the command to compile the script with arduino-cli
            upload_cmd (string): the command to upload the script with arduino-cli
        Return:
            boolean: status of wether upload was success or not
        """

        compile_process = subprocess.Popen(
            compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        compile_output = compile_process.communicate()

        if "Error during build" not in compile_output:
            upload_process = subprocess.Popen(
                upload_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            upload_output = upload_process.communicate()

            print(upload_output)

        print(compile_output)

        return True
