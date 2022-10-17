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
        self.terminal_string = ""
        self.error_string = ""

        self.top_graph_data = []
        self.bottom_graph_data = []

        self.terminal_data_list = []

    def get_new_terminal_data(self, new_data):
        """
        this function grabs new terminal data
        """

        self.terminal_data_list.append(f"{new_data}<br>")

        print(new_data)
        while len(self.terminal_data_list) >= 50:
            self.terminal_data_list.pop(0)

    def get_new_graph_data(self, top_graph_data, bottom_graph_data):
        """
        this functions grabs new data for both graphs
        """

        self.top_graph_data.append(top_graph_data)
        self.bottom_graph_data.append(bottom_graph_data)

    def get_terminal_string(self, screen_height=0):
        """
        gets the terminal strings and displays them on the screen
        """

        return screen_height
