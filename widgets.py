"""
A file to handle receiving and parsing graphing data and to
display the data onto a graph.

TODO class DeviceManagerWindow
TODO class FileManagerWindow
TODO class RecordLight
"""

import time

from bs4 import BeautifulSoup
import pyqtgraph as pg
import numpy as np

from PyQt5 import QtWidgets as qtw

# Constant list of colour orders for the graphs
COLOUR_ORDER = ["#FF0C0C",
                "#31f78e",
                "#02acf5",
                "#fc7703",
                "#9d03fc",
                "#fce803",
                "#fc03b1"]

class Graph:
    """
    Sets up the graphing object to show it on the screen.

    Attributes:
        in_use (bool): if the data is being read
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
        self.in_use = False
        self.key = key
        self.graph_data = []
        self.plots = []
        self.labels = []

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

    def decode_graph_data(self, raw_input):
        """
        Picks out the graph data from the raw data

        Args:
            raw_input (string): raw data in the form of "g(name,1,data)t(text)g(name,2,data)"
        Returns:
            graph_data (list): holds the values for the graph
        """

        graph_data = []
        raw_list = raw_input.split("g(")

        # for each item of data
        for data in raw_list:
            data = data.split(")")
            if "t(" not in data[0] and data[0] != "" and data[0].count(',') == 2:
                valid_graph_data = data[0].replace(" ", "").split(",")
                # if the data belongs to this graph
                if valid_graph_data[1] == self.key:
                    try:
                        float(valid_graph_data[2])
                        graph_data.append(valid_graph_data[2])
                    except ValueError:
                        pass

                    # if the label is not already existing
                    if valid_graph_data[0] not in self.labels:
                        self.labels.append(valid_graph_data[0])

        return graph_data

    def set_graph_data(self, raw_data):
        """
        Gets the graph data and puts it in the form to be plotted

        Args:
            raw_data (list): a list of all raw data
        """

        # if the graph data is not being read, change it
        if not self.in_use:
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

        # remove all graphs
        for item in self.plots:
            self.graph.removeItem(item)

        # add new graphs
        for i in range(num_of_plots):
            self.plots.append(self.graph.plot([0],[0], name=self.labels[i]))

    def update_graph(self):
        """
        To update the graphs displayed on the main GUI
        """

        self.in_use = True

        # transpose the 2D list of data
        plots = list(map(list, zip(*self.graph_data)))

        # if there is a change in the number of plots, update
        if len(plots) != len(self.plots):
            self.update_plots(len(plots))

        # replace the data with the latest data
        for index, plot in enumerate(self.plots):
            # if the amount of plots is not equal throughout
            # then delete all plots and break from the update loop
            if len(plots)-1 < index:
                self.update_plots(0)
                self.plots = []
                self.labels = []
                self.graph_data = []
                break
            # update plot
            pen = pg.mkPen(color=COLOUR_ORDER[index%len(COLOUR_ORDER)])
            plot.setData(np.array(plots[index], dtype=float), pen=pen)

        self.in_use = False


class Widgets:
    """
    Super class to DeviceManagerWindow, FileManagerWindow, and RecordLight

    Attributes:
        show (bool): whether or not to display the GUI
        width (int): the width of the widget
        height (int): the height of the widget

    Methods:
        get_show:
            Returns:
                bool: whether or not to show the GUI
        get_height:
            Returns:
                int: the height of the widget
        get_width:
            Returns:
                int: the width of the widget
    """

    def __init__(self, state=False, width=0, height=0):
        self.show = state
        self.width = width
        self.height = height

    def update_show(self):
        """
        converts show to not show
        """
        self.show = not self.show

    def get_show(self):
        """
        Returns:
            bool: whether or not to show the GUI
        """
        return self.show

    def get_height(self):
        """
        Returns:
            int: the height of the widget
        """
        return int(self.height)

    def get_width(self):
        """
        Returns:
            int: the width of the widget
        """
        return int(self.width)

class RecordLight(Widgets):
    """
    Blinks the record light
    This class inherits Widgets

    Attributes:
        blinking (bool): wether or not the record light is meant to blink
        running (bool): while the the app is running

    Methods:
        threaded_blink:
            blinks the light every 0.5 seconds

        update_recording:
            changes the recording status

        terminate_record:
            stops the threaded loop
    """

    def __init__(self):
        super().__init__(True)

        self.blinking = False
        self.running = True

    def threaded_blink(self):
        """
        blinks the light every 0.5 seconds
        """
        while self.running:
            if self.blinking:
                self.update_show()
            else:
                self.show = True

            time.sleep(0.75)

    def update_recording(self):
        """
        changes the recording status
        """
        self.blinking = not self.blinking

    def terminate_record(self):
        """
        stops the threaded loop
        """
        self.running = False

class SideMenu:
    """
    A class to control showing and hiding menus.

    Attributes:
        widgets_file (list): a list of widgets for the file side menu
        widgets_device (list): a list of widgets for the device side menu
        layout (pyqt layout): the layout that holds both side menus
        showing_file (bool): whether the file widgets are being shown
        showing_device (bool): whether the device widgets are being shown
    
    Methods:
        show_side_menu:
            Updates the side menu to show the correct one.

            Args:
                file (bool) whether to update file being displayed
                device (bool) whether to update device being displayed
        
        hide_menu:
            Hides the entire display (used on startup).
    """

    def __init__(self, widgets_file:list, widgets_device:list, layout):

        self.widgets_file = widgets_file
        self.widgets_device = widgets_device
        self.layout = layout

        self.showing_file = False
        self.showing_device = False

    def show_side_menu(self, file=False, device=False):
        """
        Updates the side menu to show the correct one.

        Args:
            file (bool) whether to update file being displayed
            device (bool) whether to update device being displayed
        """
        if file:
            self.showing_file = not self.showing_file
            self.showing_device = False
        elif device:
            self.showing_device = not self.showing_device
            self.showing_file = False

        self.layout.setVisible(
            self.showing_file or self.showing_device)

        for item in self.widgets_device:
            item.setVisible(self.showing_device)

        for item in self.widgets_file:
            item.setVisible(self.showing_file)

    def hide_menu(self):
        """
        Hides the entire display (used on startup).
        """
        self.layout.setVisible(False)


class CheckBox:
    """
    Creates a checkbox which uses a text browser + html to create a
    good looking way of displaying all relevant information.

    Attributes:
        name (str) : the title of the html
        vertical_layout (QVBoxLayout) : the vertical layout all the elements gfo in
        versions (QComboBox) : the drop down menu
        install (QPushButton) : the button to install
        horizontal_layout (QHBoxLayout) : the horizontal layout
        info (QTextBrowser) : the QTextBrowser that shows the HTML

    Methods:
        get_height:
            Approximates the height the HTML will take up
        
        get_version:
            Returns the currently selected version
    """

    def __init__(self, name:str, html:str, versions:list, parent=None):

        self.name = name

        self.vertical_layout = qtw.QVBoxLayout()

        self.versions = qtw.QComboBox()
        for item in reversed(versions):
            self.versions.addItem(item)

        self.install = qtw.QPushButton("Install")

        if parent:
            self.install.clicked.connect(lambda: parent.install(self.get_version(),
                                                                self.name))
        self.vertical_layout.addWidget(self.install)
        self.vertical_layout.addWidget(self.versions)

        self.horizontal_layout = qtw.QHBoxLayout()

        self.info = qtw.QTextBrowser()
        self.info.setHtml(html)
        self.info.setOpenExternalLinks(True)
        self.info.setMinimumHeight(self.get_height(html, self.info.size().width()))

        self.horizontal_layout.addLayout(self.vertical_layout)
        self.horizontal_layout.addWidget(self.info)

    def get_height(self, html:str, width:int) -> int:
        """
        test

        Args:
            html (str): the html that formats the textbox
            width (int): the width of the window

        Returns:
            int: the height of the text box *THIS IS AN ESTIMATE*
        """
        total = html.count("</p>")

        html = html.replace("<br>", "\n")
        html = html.replace("</p>", "\n")
        soup = BeautifulSoup(html, 'html.parser')
        plain_text = soup.get_text(separator=' ')

        plain_text = [item for item in plain_text.split("\n") if item != ""]

        for string in plain_text:
            total += 1
            if len(string) > 0:
                total += (len(string) * 24) // width

        return total * 20 + 50

    def get_version(self) -> str:
        """
        Returns:
            str: the string of the currently selected version
        """
        return str(self.versions.currentText())
