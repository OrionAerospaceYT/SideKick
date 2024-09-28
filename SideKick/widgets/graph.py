import pyqtgraph as pg
import numpy as np

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
        self.graph_data = []
        self.plots = []
        self.labels = []
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

        self.graph_data = []
        self.plots = []
        self.labels = []

    def decode_graph_data(self, raw_input:str) -> list:
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_data (list): holds the values for the graph
        """

        raw_list = []
        graph_data = []
        raw_input = raw_input.split(GRAPH_BEGINNING)

        for i, data in enumerate(raw_input):
            if GRAPH_ENDING in data:
                raw_list.append(raw_input[i].split(GRAPH_ENDING)[0])

        for graph in raw_list:

            graph = graph.split(",")
            name, key, data = graph[0], graph[1], graph[2]

            if key != self.key:
                continue

            if name not in self.labels:
                self.labels.append(name)

            is_num = data.replace("-", "").replace(".", "").isnumeric()

            if -1 < data.count("-") < 2 and -1 < data.count(".") < 2 and is_num:
                graph_data.append(float(data))
            else:
                graph_data.append(np.nan)
                print(f"<<< ERROR >>> Decoding graph data! {raw_input}")

        return graph_data

    def set_graph_data(self, raw_data:list):
        """
        Gets the graph data and puts it in the form to be plotted

        Args:
            raw_data (list): a list of all raw data
        """

        if not raw_data:
            return

        plots = []

        for data in raw_data:
            data = self.decode_graph_data(data)
            if data:
                for i, point in enumerate(data):
                    if i < len(plots):
                        plots[i].append(point)
                    else:
                        plots.append([point])

        for i, plot in enumerate(plots):
            if i < len(self.graph_data):
                self.graph_data[i] += plot
                while len(self.graph_data[i]) > NUM_OF_DATA_PTS:
                    self.graph_data[i].pop(0)
            else:
                self.graph_data.append(plot)

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
        for i in range(num_of_plots):
            self.plots.append(self.graph.plot([0],[0], name=self.labels[i]))
            self.graph_data[i] = self.default_data

    def update_graph(self):
        """
        To update the graphs displayed on the main GUI
        """
        if len(self.graph_data) > 0:
            print("INFO:")
            print(len(self.graph_data))
            print(len(self.graph_data[0]))

        # if there is a change in the number of plots, update
        if len(self.graph_data) != len(self.plots):
            self.update_plots(len(self.graph_data))

        # replace the data with the latest data
        for index, plot in enumerate(self.plots):
            # if the amount of plots is not equal throughout
            # then delete all plots and break from the update loop
            if len(self.graph_data)-1 < index:
                self.update_plots(0)
                self.plots = []
                self.labels = []
                self.graph_data = []
                break
            # update plot
            pen = pg.mkPen(color=COLOUR_ORDER[index%len(COLOUR_ORDER)])
            plot.setData(np.array(self.graph_data[index], dtype=float), pen=pen)
            print(self.graph_data[index])
