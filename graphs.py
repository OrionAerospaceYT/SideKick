"""
A file to handle receiving and parsing graphing data and to
display the data onto a graph.
"""

import pyqtgraph as pg

class Graph():
    """
    Sets up the graphing object to show it on
    the screen
    """

    def __init__(self):

        self.legend = None
        self.plots = None
        self.graph = None

        self.graph = pg.PlotWidget()
        self.graph.setMenuEnabled(False)

        self.legend = self.graph.addLegend()
        self.plots = []

        self.graph.setBackground('#2b2b35')

        self.legend.setLabelTextColor("#FFFFFF")
        self.graph.getAxis(
            'left').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.graph.getAxis("left").setTextPen((255, 255, 255))
        self.graph.getAxis("bottom").setTextPen((255, 255, 255))

    def update_graph(self):
        """
        TODO display new data on the graph
        """

        pass

    def set_data(self):
        """
        TODO set the new data for the graph
        """

        pass