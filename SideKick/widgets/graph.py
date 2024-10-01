import pyqtgraph as pg
import numpy as np
import re

from SideKick.globals import GRAPH_BEGINNING, GRAPH_ENDING
from SideKick.globals import NUM_OF_DATA_PTS, COLOUR_ORDER

class Graph:
    """
    Sets up the graphing object to show it on the screen.

    Attributes:
        key (string): the string that says the data belongs to the graph
        graph_data (list): all of the graph data for this graph
        plots (list): the plots on the pyqtgraph object
        labels (list): the label for each variable on the graph
        graph (pyqtgraph): the graph object
        legend (pyqtgraph.addLegend): the style of the graph

    Methods:
        decode_graph_data:
            Picks out the graph data from the raw data

            Args:
                raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
            Returns:
                graph_data (list): holds the values for the graph

        set_graph_data:
            Gets the graph data and puts it in the form to be plotted

            Args:
                raw_data (list): a list of all raw data

        update_plots:
            Adds or removes old plots.

            Args:
                num_of_plots (int): the number of plots

        update_graph:
            To update the graphs displayed on the main GUI
    """

    def __init__(self, key="0"):
        # variable definitions
        self.resize = True
        self.key = key
        self.graph_data = {}
        self.plots = []
        self.default_data = [0 for _ in range(NUM_OF_DATA_PTS)]

        # pyqtgraph definitions
        self.graph = pg.PlotWidget()
        self.legend = self.graph.addLegend()

        # Modify look of graphs
        self.graph.setMenuEnabled(False)
        self.graph.setBackground('#2b2b35')
        self.legend.setLabelTextColor("#FFFFFF")
        self.graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis("left").setTextPen((255, 255, 255))
        self.graph.getAxis("bottom").setTextPen((255, 255, 255))

    def clear_graph(self):
        """
        Removes all data from graph
        """
        for item in self.plots:
            self.graph.removeItem(item)

        self.graph_data = {}
        self.plots = []

    def is_graphable(self, data):
        """
        Check if the data from the device is numeric and able to be graphed.

        Args:
            data (string): the data to be tested

        Returns:
            bool: whether the data is graphable or not
        """
        is_num = data.replace("-", "").replace(".", "").isnumeric()
        if -1 < data.count("-") < 2 and -1 < data.count(".") < 2 and is_num:
            return True
        return False

    def decode_graph_data(self, raw_input:str) -> list:
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_data (list): holds the values for the graph
        """
        # Define the regex pattern
        pattern = f'{GRAPH_BEGINNING}([^z]+),(\\d+),([^z]+){GRAPH_ENDING}'
        decoded_data = re.findall(pattern, raw_input)
        graph_data = [list(data) for data in decoded_data]
        indeces_to_be_deleted = []

        # Go through the list and remove unrelated data from this graph then
        # check that the remaining data is graphable and remove the key
        for i, graph in enumerate(graph_data):

            key, data = graph[1], graph[2]

            if key != self.key:
                indeces_to_be_deleted.append(i)

            if not self.is_graphable(data):
                graph_data[i][2] = np.nan
                #print(f"<<< ERROR >>> Decoding graph data! {raw_input}")
            graph_data[i].pop(1)

        # Delete the unrelated data
        for indx in reversed(indeces_to_be_deleted):
            graph_data.pop(indx)

        return graph_data

    def set_graph_data(self, raw_data:list):
        """
        Gets the graph data and puts it in the form to be plotted

        Args:
            raw_data (list): a list of all raw data
        """

        if not raw_data:
            return

        data = "".join(raw_data)
        graph_data = self.decode_graph_data(data)

        for label, data in graph_data:
            if label not in self.graph_data.keys():
                self.graph_data[label] = [np.nan for _ in range(NUM_OF_DATA_PTS)]
            self.graph_data[label].append(data)
            while len(self.graph_data[label]) > NUM_OF_DATA_PTS:
                self.graph_data[label].pop(0)

    def update_plots(self, num_of_plots:int):
        """
        Adds or removes old plots.

        Args:
            num_of_plots (int): the number of plots
        """
        # remove all graphs
        for item in self.plots:
            self.graph.removeItem(item)

        # add new graphs
        for i, label in enumerate(self.graph_data.keys()):
            self.plots.append(self.graph.plot([0],[0], name=label))
            #self.graph_data[i] = self.default_data

    def update_graph(self):
        """
        To update the graphs displayed on the main GUI
        """
        # if there is a change in the number of plots, update
        if len(self.graph_data.keys()) != len(self.plots):
            self.update_plots(len(self.graph_data))

        # replace the data with the latest data
        for indx, (plot, key) in enumerate(zip(self.plots, self.graph_data.keys())):
            pen = pg.mkPen(color=COLOUR_ORDER[indx%len(COLOUR_ORDER)])
            plot.setData(np.array(
                self.graph_data[key], dtype=float), pen=pen)
