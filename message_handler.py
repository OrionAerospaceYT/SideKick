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

        # intial change
        error = error.replace("\n", "<br>")

        is_error = False
        is_warning = False
        is_note = False

        debug_output = ""

        # colouring error/warnings
        for line in error.split("<br>"):
            if "error" in line:
                line = line.replace("error", "<font color=#E21919>error")
                is_error = True
            elif is_error and "In file" in line:
                line = line.replace(
                    "In file", "<font color=#FFFFFF>In file")
                is_error = False
            elif is_error and r"C:\Users" in line:
                line = line.replace(
                    r"C:\Users", r"<font color=#FFFFFF>C:\Users")
                is_error = False

            if "warning" in line:
                line = line.replace(
                    "warning", "<font color=#D6790F>warning")
                is_warning = True
            elif is_warning and "In file" in line:
                line = line.replace(
                    "In file", "<font color=#FFFFFF>In file")
                is_warning = False
            elif is_warning and r"C:\Users" in line:
                line = line.replace(
                    r"C:\Users", r"<font color=#FFFFFF>C:\Users")
                is_warning = False

            if "note" in line:
                line = line.replace("note", "<font color=#00f0c3>note")
                is_note = True
            elif is_note and "In file" in line:
                line = line.replace(
                    "In file", "<font color=#FFFFFF>In file")
                is_note = False
            elif is_note and r"C:\Users" in line:
                line = line.replace(
                    r"C:\Users", r"<font color=#FFFFFF>C:\Users")
                is_note = False

            debug_output += line + "<br>"

        # trailing sections
        debug_output = debug_output.replace("[0m", "<font color=\"#ffffff\">")
        debug_output = debug_output.replace(
            "[90m", "<font color=\"#D6790F\">")
        debug_output = debug_output.replace(
            "[92m", "<font color=\"#00f0c3\">")
        self.debug_html = debug_output.replace(
            "[93m", "<font color=\"#00f0c3\">")
