from distutils.command.upload import upload
import numpy as np
from datetime import datetime
import random
import time
import sys
import os
import subprocess
import glob
import serial
import __main__

class DataHandler():

    def __init__(self):

        # Define default variables here, by default, xyz plots.
        self.com_port = ""
        self.com = False
        self.device = None
        self.labels =[[],[]]
        self.num_of_top_plots = 0
        self.num_of_bottom_plots = 0
        self.top_plots_raw_data = []
        self.top_plots_data = []
        self.top_plots = []
        self.bottom_plots_raw_data = []
        self.bottom_plots_data = []
        self.bottom_plots = []
        self.terminal_data = []
        self.buffer_string = ""
        self.number_of_lines_displayed_on_terminal = 20
        self.amount_of_data = 1000
        self.skipped_loops = 0
        self.html_header = """<h1><b><font color="#00f0c3">Terminal</b></h1><body>"""
        self.html_footer = "</font></body>"
        self.save_data = False
        self.com_port_range = 0
        self.html_terminal_text  = self.html_header + self.html_footer
        self.serial_port = []
        self.errors = False

    # Goes through raw terminal input and outputs the graphing values in a list.
    # The list has a format of [name, 1 for top - 2 for bottom, data]
    def decode_graph(self, input):

        # edmpty list for output values
        output = []

        # decodes the input data from sidekick format to usable data
        graph_data = input.split("g(")

        # goes through each item and keeps breaking it down
        for item in graph_data:

            # splits into ended sections
            item = item.replace(" ", "")
            item = item.split(")")

            # removes empty lists : checks that we dont add a terminal to graphs so terminal can be anywhere
            if item != [''] and "t(" not in item[0] and "r(" not in item[0]:

                output.append(item[0].split(","))

        graph_data = []

        for x in range(0, len(output)):
            i = []

            for item in output[x]:
                value = item

                ## checks if the data is a number
                if value.isnumeric():
                    item = float(item)

                # assembles the array of data to add to graph_data
                i.append(item)

            graph_data.append(i)

        # checks for all inputs to graphs to be numerical
        for x in range(0,len(graph_data)):
            for y in range(1, len(graph_data[0])):
                try:  # .isnumeric wont work on already numeric numbers
                    float(graph_data[x][y])
                except:
                    del graph_data[x] # deletes item with unwanted data

        return graph_data

    # Returns terminal text as string.
    def decode_terminal(self, input):

        # terminal section of decoding
        raw_list = input.split("t(")
        terminal_output = []

        for string in raw_list:
            # finds which seperation the terminal is in
            if string != '':
                string = string.split(")")
                for data in string:
                    if "g(" not in data and "r(" not in data:
                        if data != "" and "\r" not in data:
                            terminal_output.append(data)
        #__main__.fileManager.save_terminal_data(terminal_output)

        return terminal_output

    # Returns list of [x, y, z] orientation
    def decode_orientation(self, input):
        # orientation section of decoding
        orientation_output = input.split("r(")

        for item in orientation_output:

            # finds which seperation the orientation is in
            if item != '':
                item = item.split(")")
                for item in item:
                    if "g(" not in item and "t(" not in item:
                        orientation_output = item
                        break

        if len(orientation_output.split(",")) == 3:
            return orientation_output.split(",")
        else:
            return [0,0,0]

    def transpose(self, list):

        list = np.array(list)
        transpose = list.T

        return transpose.tolist()

    # Formats the terminal data as html for the PyQt5 textBox
    def organise_terminal_data(self, terminal_parsed_data_string):

        # Gets current date and time
        now = datetime.now()
        current_time_string = now.strftime("%H:%M:%S")

        # Creates string of "time,data"
        for item in terminal_parsed_data_string:
            self.terminal_data.append(current_time_string + "," + item)

        # Keeps terminal data string at length of data to be displayed as screen changes
        while len(self.terminal_data) > self.number_of_lines_displayed_on_terminal:
            self.terminal_data.pop(0)

        # Terminal title for text box
        self.html_terminal_text = self.html_header

        # For each line, makes the time as white and data as #00f0c3
        for mesage in self.terminal_data:
            text_for_terminal_and_time = mesage.split(",")
            self.html_terminal_text += (f"""<p><font color="white">{text_for_terminal_and_time[0]}>$ <font color="#00f0c3">{text_for_terminal_and_time[1]}</p>""")

        # Ends the html
        self.html_terminal_text += self.html_footer

    # Returns a list of open serial ports
    def serial_ports(self):

        # Checks the supported OS: windows linux and darwin
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        start = time.time()

        # Checks if the port is open, then appends to list
        port = ports[self.com_port_range]
        try:
            s = serial.Serial(port)
            s.close()
            self.serial_port.append(port)
        except (OSError, serial.SerialException):
            if port in self.serial_port:
                self.serial_port.remove(port)

        if self.com_port_range == len(ports) - 1:
            self.com_port_range = 0
        else:
            self.com_port_range += 1

        return self.serial_port

    # The function that gets called and uses the other functions.
    def get_data(self):
        # Checks if device has been defined and if it has, gets the data from the serial device
        if self.device != None:
            self.buffer_string = self.buffer_string + self.device.read(self.device.inWaiting()).decode().strip()
        # Keeps buffer size small to save memory.
        # Saves two lines as one is complete and the other may be incomplete.
        if len(self.buffer_string.split("\r")) > 3:
            raw_data = self.buffer_string.split("\r")[-3]
            self.buffer_string = self.buffer_string.split("\r")[-3]
        else:
            raw_data = ""

        # Keeps trying to connect to serial device if none is connected
        try:
            if self.device == None:
                self.device = serial.Serial(self.com_port, __main__.eventHandler.graphing.ui.baud_rate.currentText(), rtscts=False)
        except:
            pass

        # If there is raw_data then we need to display it.
        if not len(raw_data) > 0:
            self.skipped_loops += 1
            return 0

        self.skipped_loops = 0

        # Parses all of the data seperately: graph, terminal and orientation.
        graph_data = self.decode_graph(raw_data)
        terminal_output = self.decode_terminal(raw_data)
        orientation_output = self.decode_orientation(raw_data)

        # Formats the html for the terminal data.
        self.organise_terminal_data(terminal_output)

        # Saves data to file if recording is meant to happen.
        if self.save_data:
            for item in terminal_output:
                __main__.fileManager.save_terminal_data(item)
        # Sets the orientation equal to the latest
        self.x , self.y , self.z = orientation_output[0], orientation_output[1], orientation_output[2]

        # Defines the temporary list that we append data to
        top_temp , bottom_temp = [], []

        # Starts off with no plots on top or bottom...
        # We use this to ensure that the displayed number of plots equals
        # the number of input plots.
        self.num_of_top_plots, self.num_of_bottom_plots = 0, 0

        self.labels = [[],[]]

        # Goes through graph data and checks which graph, the label and values
        for item in graph_data:
            try:
                if item[1] == 1:
                    top_temp.append(float(item[2]))
                    self.num_of_top_plots += 1
                    self.labels[0].append(item[0])
                elif item[1] == 2:
                    bottom_temp.append(float(item[2]))
                    self.num_of_bottom_plots += 1
                    self.labels[1].append(item[0])
            except:
                pass

        # Appends latest data to current data buffer of 200.
        # If the buffer is too long, remove the first element.
        self.top_plots_raw_data.append(top_temp)

        if len(self.top_plots_raw_data) > self.amount_of_data:
            self.top_plots_raw_data.pop(0)

        self.top_plots_data = self.transpose(self.top_plots_raw_data)

        self.bottom_plots_raw_data.append(bottom_temp)

        if len(self.bottom_plots_raw_data) > self.amount_of_data:
            self.bottom_plots_raw_data.pop(0)

        self.bottom_plots_data = self.transpose(self.bottom_plots_raw_data)

    # Uploads the selected project to the board.
    def compile_and_upload(self, port, project):

        # Gets the board from the board selected in drop down.
        if __main__.eventHandler.graphing.ui.device.currentText() != "Select Board":
            board = __main__.supported_devices[__main__.eventHandler.graphing.ui.device.currentText()]

            cwd = os.getcwd()
            # Compiles the coad before upload and gets errors:
            compile_cmd = f'"{cwd}/Externals/arduino-cli.exe" compile --fqbn {board} {project}.ino'
            compile = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            self.compile_output, error = compile.communicate()

            print(compile_cmd)
            print(self.compile_output)

            # Uploads the code and gets errors.
            upload_cmd = f'"{cwd}/Externals/arduino-cli.exe" upload -p {port} --fqbn {board} {project}.ino'
            upload = subprocess.Popen(upload_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            self.upload_output, error = upload.communicate()

            print(upload_cmd)
            print(self.upload_output)
        # If no board is selected, displays error.
        else:
            __main__.data.html_header = f"""<h1><b><font color="#00f0c3">Terminal</b></h1><body>
                                           <p><font color="#FF0C0C">Please select a board.</p>"""

    # Returns the HTML for the errors to be displayed.
    def process_errors(self):
        if "error" in str(self.compile_output):
            # Formats the output for html rather than python
            output = self.compile_output.decode('utf-8').replace("\r\n", "<br>")

            # Defines temporary variables
            error = False
            warning = False
            self.compile_output = ""

            # Defines colours
            error_colour = "#ff003c"
            warning_colour = "#ff7300"
            default_colour = "#00c0f0"

            # Iterates through each line to check for error
            for item in output.split("<br>"):
                # Checks for errors
                if "error" in item:
                    item = f"""<font color={error_colour}>{item}<font color="#00f0c3">"""
                    error = True
                elif error:
                    item = f"""<font color={error_colour}>{item}<font color="#00f0c3">"""
                    if "^" in item:
                        error = False
                # Checks for warnings
                elif "warning" in item:
                    item = f"""<font color={warning_colour}>{item}<font color="#00f0c3">"""
                    warning = True
                elif warning:
                    item = f"""<font color={warning_colour}>{item}<font color="#00f0c3">"""
                    if "^" in item:
                        warning = False
                # Information lines are default
                else:
                    item = f"""<font color={default_colour}>{item}<font color="#00f0c3">"""
                self.compile_output += item
            return True
        else:
            return False

    # This code runs upload on another thread to keep GUI on main thread
    def upload(self, port, project):

        # Compiles and Uploads the project.
        self.compile_and_upload(port, project)

        # Parses Errors for the GUI to display.
        if self.process_errors():
            self.errors = True
        else:
            __main__.eventHandler.update_com(port)
