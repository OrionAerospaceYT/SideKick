"""
This file handles displaying error messages and graphs
This file imports device manager and gets the data
"""

COLOUR_ORDER = ["#FF0C0C",
                "#31f78e",
                "#02acf5",
                "#fc7703",
                "#9d03fc",
                "#fce803",
                "#fc03b1"]

ACCENT_COLOUR = "#252530"
TEXT_COLOUR = "#00f0c3"


class MessageHandler():
    """
    Gets all text/graph data to be displayed on the front end
    """

    def __init__(self):

        self.raw_data = []

        self.terminal_header = "<h1><p style=\"color:#00f0c3;font-size:30px\">Terminal</p></h1><br>"
        self.terminal_html = ""
        self.error_string = ""
        self.debug_html = ""

        self.status_trail = [".", ".", "."]
        self.status_increasing = False

        self.beginning = """<p><font color="#00f0c3">$> <font color="#FFFFFF">"""
        self.ending = "</p>"

        self.top_graph_data = []
        self.bottom_graph_data = []

        self.terminal_data_list = []

    def decode_graph_data(self, raw_input):
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_top_data (list): holds the values for the top graph
            graph_bottom_data (list): holds the values for the bottom graph
        """

        graph_top_data = []
        graph_bottom_data = []
        raw_list = raw_input.split("g(")

        for data in raw_list:

            data = data.split(")")

            if "t(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                valid_graph_data = data[0].replace(" ", "").split(",")
                if valid_graph_data[1] == "1":
                    graph_top_data.append(valid_graph_data[2])
                else:
                    graph_bottom_data.append(valid_graph_data[2])

        return graph_top_data, graph_bottom_data

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

    def terminal_output_html(self, height):
        """
        Calculates the amount of lines the terminal can displaye at
        once (TODO)

        Args:
            height (int): the height of the terminal
        """
        decoded_data = []

        amount_of_data = int(height / 30)

        for i in range(1, amount_of_data):
            if i > len(self.raw_data):
                break
            decoded_string = self.decode_terminal_data(self.raw_data[-i])
            decoded_data.append(decoded_string)

        terminal_html = self.terminal_header

        for data in decoded_data:
            terminal_html += self.beginning + data + self.ending

        self.terminal_html = terminal_html

    def decode_debug_message(self, error):
        """
        Converts the dull default compile/upload output to nice coloured html
        for easy debugging in the debug window

        Args:
            error (string): the error from the compile/upload from arduino-cli
        """

        error = error.replace("\n", "<br>")

        debug_output = ""

        for line in error.split("<br>"):
            line = line.replace("error:", "<font color=#E21919>error:")

            line = line.replace(
                "warning:", "<font color=#D6790F>warning:")

            line = line.replace("note:", "<font color=#00f0c3>note:")

            line = line.replace(
                "In file", "<font color=#FFFFFF>In file")
            line = line.replace(
                r"C:\Users", r"<font color=#FFFFFF>C:\Users")
            line = line.replace("^", "^<font color=#FFFFFF>")

            debug_output += line + "<br>"

        debug_output = debug_output.replace(
            "\x1B[0m", "<font color=\"#ffffff\">")
        debug_output = debug_output.replace(
            "\x1B[90m", "<font color=\"#D6790F\">")
        debug_output = debug_output.replace(
            "\x1B[92m", "<font color=\"#00f0c3\">")
        self.debug_html = debug_output.replace(
            "\x1B[93m", "<font color=\"#00f0c3\">")

    def update_ellipsis(self):
        """
        Either increases or decreases the number of dots at the end of the uploading
        or compiling message to show that the gui is working.
        """

        length = len(self.status_trail)

        if length <= 1 and not self.status_increasing:
            self.status_increasing = True
        elif length >= 3 and self.status_increasing:
            self.status_increasing = False

        if self.status_increasing:
            self.status_trail.append(".")
        else:
            self.status_trail.pop(0)

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
