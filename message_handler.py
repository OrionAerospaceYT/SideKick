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
