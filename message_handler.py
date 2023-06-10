"""
This file handles displaying error messages and graphs
This file imports device manager and gets the data
"""

import time

ACCENT_COLOUR = "#252530"
TEXT_COLOUR = "#00f0c3"

TERMINAL_HEADER = "<h1><p style=\"color:#00f0c3;font-size:30px\"\
>Terminal</p></h1><div style=\"margin-top:75px;\"></div>"

SUCCESS_MSG = "<p style=\"font-weight:bold; color:#00f0c3; font-size:24px\">\
Success</p><div style=\"margin-top:150px;\"></div>"

FAILURE_MSG = "<p style=\"font-weight: bold;color:#E21919; font-size:24px\">\
Error</p><div style=\"margin-top:150px;\"></div>"

USER_MESSAGE = "<p style=\"font-weight: bold;color:#34c0eb; font-size:24px\">\
User command</p><div style=\"margin-top:150px;\"></div>"

ERROR_TERMS = ["Error opening sketch", "Error during build", "exit status"]

class MessageHandler():
    """
    Gets all text/graph data to be displayed on the front end
    """

    def __init__(self, layout, widget, expansion_widgets=None, line_edit=None):

        self.debug_window = False
        self.minimized = True
        self.widget = widget
        self.layout = layout
        self.expansion_widgets = expansion_widgets
        self.line_edit = line_edit

        self.terminal_html = ""
        self.error_string = ""
        self.debug_html = ""

        self.status_trail = [".", ".", "."]
        self.status_increasing = False
        self.running = True

        self.beginning = """<p><font color="#00f0c3">$> <font color="#FFFFFF">"""
        self.ending = "</p>"

    def decode_terminal_data(self, raw_input):
        """
        Combines all terminals in one message to a single line for terminal

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            terminal_data (strig): a single line string to have html added to it later
        """
        raw_list = raw_input.split("t(")
        terminal_data = ""

        for data in raw_list:
            data = data.split(")")
            if "g(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                terminal_data += " " + data[0]

        return terminal_data

    def get_terminal(self, raw_data, size=(0,0), live=True):
        """
        Calculates the amount of lines the terminal can display at
        once.

        Args:
            raw_data (list): a list of all raw data
            size (tuple): the x and y dimensions of the terminal
            live (bool): if the data is being live streamed
        """
        decoded_data = []
        total_lines = 0

        for item in raw_data:
            decoded_string = self.decode_terminal_data(item)
            if len(decoded_string) != 0:
                decoded_data.append(decoded_string)

        terminal_html = TERMINAL_HEADER

        # if live data, it cannot be scrolled through so it must be limited
        # to the screen
        if live:
            amount_of_lines = int((size[0]-32) / 18)

            for data in reversed(decoded_data):
                total_lines += len(data) // (size[1] / 8) + 2
                if total_lines <= amount_of_lines:
                    terminal_html += self.beginning + data + self.ending

        # if not live data then all data is shown in one go
        if not live:
            for data in decoded_data:
                terminal_html += self.beginning + data + self.ending

        self.terminal_html = terminal_html

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

        debug_output = debug_output.replace("\x1B[0m", "<font color=\"#ffffff\">")
        debug_output = debug_output.replace("\x1B[90m", "<font color=\"#D6790F\">")
        debug_output = debug_output.replace("\x1B[92m", "<font color=\"#00f0c3\">")
        debug_output = debug_output.replace("\x1B[93m", "<font color=\"#00f0c3\">")
        debug_output = debug_output.replace("<br><br><br>", "<br>")

        for item in ERROR_TERMS:
            if item in debug_output:
                return debug_output + FAILURE_MSG

        return debug_output + SUCCESS_MSG


    def decode_debug_message(self, error, cmd_type):
        """
        Converts the dull default compile/upload output to nice coloured html
        for easy debugging in the debug window

        Args:
            error (string): the error from the compile/upload/user from arduino-cli
            cmd_type (string): the type of command e.g. usr
        """
        error = error.replace("\n", "<br>")

        if ("compile", "upload") in cmd_type:
            html = self.format_compile_and_upload(error)
        else:
            html = error + USER_MESSAGE
        self.debug_html += html

        self.set_debug_html()

    def set_debug_html(self):
        """
        Displays the html on the debug window text browser.
        """
        self.widget.setHtml(self.debug_html)
        self.debug_window = True
        self.layout.setVisible(self.debug_window)
        time.sleep(0.1)
        self.widget.verticalScrollBar().setValue(self.widget.verticalScrollBar().maximum()-50)

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

    def expand_debug(self, exception=False):
        """
        Either hides all graphing and terminal if expand or
        shows all graphing and terminal if minimize.
        """

        if not self.debug_window and not exception:
            return

        if self.minimized:
            self.line_edit.setPlaceholderText("Enter arduino-cli message here.")
            for item in self.expansion_widgets:
                item.setVisible(False)
        else:
            self.line_edit.setPlaceholderText("Enter device message here.")
            for item in self.expansion_widgets:
                item.setVisible(True)
        self.minimized = not self.minimized
