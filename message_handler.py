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

        self.terminal_header = """<h1><p style="color:#00f0c3;font-size:30px">Terminal</p></h1>"""
        self.terminal_string = ""
        self.error_string = ""

        self.top_graph_data = []
        self.bottom_graph_data = []

        self.terminal_data_list = []

    def decode_graph_data(self, raw_input):
        """
        parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        to graph_top_data, graph_bottom_data which are lists
        example graph output would be: [[1,2,3,4,5,],[5,4,3,2,1],[2,5,4,1,3]]

        this data still needs to be processed as it is in string form
        the processing will go in the main backend
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
        parses the raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        to terminal_data which is a string
        all terminal data from one output is put into a single line
        """

        raw_list = raw_input.split("t(")
        terminal_data = ""

        for data in raw_list:
            data = data.split(")")
            if "g(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                terminal_data += " " + data[0]

        return terminal_data
