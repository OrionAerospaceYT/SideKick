"""
A file to handle receiving and parsing graphing data and to
display the data onto a graph.
"""

import pyqtgraph as pg
import numpy as np

COLOUR_ORDER = ["#FF0C0C",
                "#31f78e",
                "#02acf5",
                "#fc7703",
                "#9d03fc",
                "#fce803",
                "#fc03b1"]

class Graph():
    """
    Sets up the graphing object to show it on
    the screen
    """

    def __init__(self, key="0"):

        self.legend = None
        self.plots = []
        self.labels = []
        self.graph = None

        self.graph = pg.PlotWidget()
        self.graph.setMenuEnabled(False)

        self.legend = self.graph.addLegend()

        self.graph.setBackground('#2b2b35')

        self.legend.setLabelTextColor("#FFFFFF")
        self.graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis("left").setTextPen((255, 255, 255))
        self.graph.getAxis("bottom").setTextPen((255, 255, 255))

        self.key = key
        self.graph_data = []

    def decode_graph_data(self, raw_input):
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_top_data (list): holds the values for the top graph
            graph_bottom_data (list): holds the values for the bottom graph
        """

        graph_data = []
        raw_list = raw_input.split("g(")

        for data in raw_list:
            data = data.split(")")
            if "t(" not in data[0] and data[0] != "" and "\r" not in data[0]:
                valid_graph_data = data[0].replace(" ", "").split(",")
                if valid_graph_data[1] == self.key:
                    graph_data.append(valid_graph_data[2])
                    if valid_graph_data[0] not in self.labels:
                        self.labels.append(valid_graph_data[0])

        return graph_data

    def set_graph_data(self, raw_data):
        """
        Gets the graph data and puts it in the form to be plotted

        Args:
            raw_data (list): a list of all raw data
        """
        self.graph_data = []

        for data in raw_data:
            plot = self.decode_graph_data(data)
            if plot:
                self.graph_data.append(plot)

    def update_plots(self, num_of_plots):
        """
        Adds or removes old plots.

        Args:
            num_of_plots (int): the number of plots
        """

        for item in self.plots:
            self.graph.removeItem(item)

        for i in range(num_of_plots):
            self.plots.append(self.graph.plot([0],[0], name=self.labels[i]))

    def update_graph(self):
        """
        To update the graphs displayed on the main GUI
        """

        plots = list(map(list, zip(*self.graph_data)))

        if len(plots) != len(self.plots):
            self.update_plots(len(plots))

        for index, plot in enumerate(self.plots):
            pen = pg.mkPen(color=COLOUR_ORDER[index%len(COLOUR_ORDER)])
            plot.setData(np.array(plots[index], dtype=float), pen=pen)


class Widgets():
    """
    super class to DevieManagerWindow, FileManagerWindow, and RecordLight
    """

    def __init__(self, state=False):
        self.show = state

class DeviceManagerWindow(Widgets):
    """
    Responsible for data on the device manager widgets.
    TODO
    """

    def __init__(self):
        super().__init__()

        self.device = ""
        self.device_list = []
        self.baud = 115200

class FileManagerWindow(Widgets):
    """
    Responsible for data on the file manager widgets.
    TODO
    """

    def __init__(self):
        super().__init__()

        self.project = ""
        self.project_list = []

class RecordLight(Widgets):
    """
    Blinks the record light
    TODO
    """

    def __init__(self):
        super().__init__(True)
