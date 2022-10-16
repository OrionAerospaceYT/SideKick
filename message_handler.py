"""
This file handles displaying error messages and graphs
This file imports device manager and gets the data
"""


class MessageHandler():
    """
    Gets all text/graph data to be displayed on the front end
    """

    def __init__(self):
        self.terminal_string = ""
        self.error_string = ""

        self.top_graph_data = []
        self.bottom_graph_data = []

    def get_new_terminal_data(self, new_data):
        """
        this function grabs new terminal data
        """

        self.terminal_string += f"{new_data}\n"

    def get_new_graph_data(self, top_graph_data, bottom_graph_data):
        """
        this functions grabs new data for both graphs
        """

        self.top_graph_data.append(top_graph_data)
        self.bottom_graph_data.append(bottom_graph_data)
