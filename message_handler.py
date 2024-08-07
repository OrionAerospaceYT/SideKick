"""
This file handles displaying error messages and graphs
This file imports device manager and gets the data
"""

import re
import time
from globals import FQBN_ERROR_TERM, SELECT_BOARD_MESSAGE
from globals import ERROR_TERMS, FAILURE_MSG, SUCCESS_MSG
from globals import GRAPH_BEGINNING, GRAPH_ENDING, USER_MESSAGE

class MessageHandler():
    """
    Gets all text/graph data to be displayed on the front end
    """

    def __init__(self, layout, widget, expansion_screen=None, line_edit=None):

        self.debug_window = False
        self.minimized = True
        self.widget = widget
        self.layout = layout
        self.expansion_screen = expansion_screen
        self.line_edit = line_edit

        self.terminal_html = ""
        self.error_string = ""
        self.debug_html = ""

        self.status_trail = [".", ".", "."]
        self.status_increasing = False
        self.running = True

        self.beginning = """<p><font color="#00f0c3">$> <font color="#FFFFFF">"""
        self.ending = "</p>"

    def get_save_html(self, raw_data):
        """
        Calculates the amount of lines the terminal can display at
        once.

        Args:
            raw_data (list): a list of all raw data
            size (tuple): the x and y dimensions of the terminal
            live (bool): if the data is being live streamed
        """
        if not raw_data:
            return

        # Make data HTML friendly
        for i, data in enumerate(raw_data):
            data = data.replace("&", "&amp;")
            data = data.replace("<", "&lt;")
            data = data.replace("\"", "&quot;")
            data = data.replace("'", "&#39;")
            raw_data[i] = data.replace(">", "&gt;")

        # Decoding the raw data
        decoded_data = []
        for item in raw_data:
            decoded_string = re.sub(f'{GRAPH_BEGINNING}.*?{GRAPH_ENDING}', '', item)
            if len(decoded_string) != 0:
                decoded_data.append(decoded_string)

        # Assemble the data from the raw data
        message_string = ""
        for data in reversed(decoded_data):
            message_string += self.beginning + data + self.ending

        # Display data
        self.terminal_html = message_string

    def clear_terminal(self):
        """
        Sets the terminal_html to just show Terminal at the top of
        the QTextBrowser
        """
        self.terminal_html = ""

    def get_line_number(self, string):
        """
        Gets the line number of the error in the compile

        Returns:
            int: the line number the error is on
        """

        pattern = r".*\\([^:]+):(\d+):\d+: <font color=#E21919>error:"
        match = re.search(pattern, string)
        if match:
            filename = match.group(1)
            first_number = int(match.group(2))
            return filename, first_number
        return -1, -1

    def format_compile_and_upload(self, error):
        """
        Formats the html for the command

        Args:
            error (string): the error from the compile/upload from arduino-cli
        """

        debug_output = ""

        for line in error.split("<br>"):
            line = line.replace("error:", "<font color=#E21919>error:")
            line = line.replace("warning:", "<font color=#D6790F>warning:")
            line = line.replace("note:", "<font color=#00f0c3>note:")
            line = line.replace("In file", "<font color=#FFFFFF>In file")
            line = line.replace(r"C:\Users", r"<font color=#FFFFFF>C:\Users")
            line = line.replace("^", "^<font color=#FFFFFF>")

            debug_output += line + "<br>"
        file_name, line_num = self.get_line_number(debug_output)

        debug_output = debug_output.replace("\x1B[0m", "<font color=\"#ffffff\">")
        debug_output = debug_output.replace("\x1B[90m", "<font color=\"#D6790F\">")
        debug_output = debug_output.replace("\x1B[92m", "<font color=\"#00f0c3\">")
        debug_output = debug_output.replace("\x1B[93m", "<font color=\"#00f0c3\">")
        debug_output = debug_output.replace("<br><br><br>", "<br>")

        if FQBN_ERROR_TERM in debug_output:
            return SELECT_BOARD_MESSAGE

        for item in ERROR_TERMS:
            if item in debug_output:
                if line_num > 0:
                    message = FAILURE_MSG + "line " + str(line_num) + " in " + str(file_name)
                    message += "</h1>"
                else:
                    message = FAILURE_MSG + "</h1>"
                return message + debug_output

        return SUCCESS_MSG + debug_output


    def decode_debug_message(self, error, cmd_type):
        """
        Converts the dull default compile/upload output to nice coloured html
        for easy debugging in the debug window

        Args:
            error (string): the error from the compile/upload/user from arduino-cli
            cmd_type (string): the type of command e.g. usr
        """
        error = error.replace("\n", "<br>")

        if cmd_type in ("compile", "upload"):
            html = self.format_compile_and_upload(error)
        else:
            html = "<font color=\"#ffffff\">" + USER_MESSAGE + error

        if error == ".<br>":
            self.debug_html = SUCCESS_MSG + "Upload done." + self.debug_html
        else:
            self.debug_html = html + self.debug_html

        self.set_debug_html()

    def set_debug_html(self):
        """
        Displays the html on the debug window text browser.
        """
        self.widget.setHtml(self.debug_html)
        self.debug_window = True
        self.layout.setVisible(self.debug_window)

    def close_debug_window(self):
        """
        Sets the state of the debug window to false
        """
        self.debug_window = False
        self.layout.setVisible(self.debug_window)
        if not self.minimized:
            self.expand_debug(exception=True)

    def update_ellipsis(self):
        """
        Either increases or decreases the number of dots at the end of the uploading
        or compiling message to show that the gui is working.
        """

        while self.running:
            length = len(self.status_trail)

            if length <= 0 and not self.status_increasing:
                self.status_increasing = True
            elif length >= 3 and self.status_increasing:
                self.status_increasing = False

            if self.status_increasing:
                self.status_trail.append(".")
            else:
                self.status_trail.pop(0)

            time.sleep(0.5)

    def get_status(self, status):
        """
        Puts self.compile and self.status into a signle screen

        Args:
            status (string): the string to add the ellipsis to
        Returns:
            status (string): the input with the elipsis on the end
        """
        for item in enumerate(self.status_trail):
            status += item[1]

        return status

    def terminate_ellipsis(self):
        """
        Ends the threaded loop
        """
        self.running = False

    def expand_debug(self, button=None, exception=False):
        """
        Either hides all graphing and terminal if expand or
        shows all graphing and terminal if minimize.
        """

        if not self.debug_window and not exception:
            return

        if self.minimized:
            if button is not None:
                button.setText("Minimize")
            self.line_edit.setPlaceholderText("Enter arduino-cli message here.")
            self.expansion_screen.setVisible(False)
        else:
            if button is not None:
                button.setText("Expand")
            self.line_edit.setPlaceholderText("Enter device message here.")
            self.expansion_screen.setVisible(True)
        self.minimized = not self.minimized
