from PyQt5 import QtCore as qtc
from PyQt5 import QtGui
from PyQt5 import QtWidgets as qtw
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import __main__

from Ui.GraphingUi import Ui_MainWindow as graphing


class Graphing(qtw.QMainWindow):

    def __init__(self, parent=None):
        self.debug = False
        self.com_port = 0
        self.i = 0
        self.blink = 0
        super(Graphing, self).__init__(parent=parent)

        # Define the gui.
        self.ui = graphing()
        self.ui.setupUi(self)

        for name in __main__.supported_devices:
            self.ui.device.addItem(name)

        cursor = self.ui.terminal.textCursor()
        cursor.clearSelection()
        self.ui.terminal.setTextCursor(cursor)

        # Set pyqtPlot to the top widget.
        self.gui_top_graph = pg.PlotWidget()
        self.ui.gui_top_graph = qtw.QVBoxLayout()
        self.ui.top_widget.setLayout(self.ui.gui_top_graph)
        self.ui.gui_top_graph.addWidget(self.gui_top_graph)
        self.top_legend = self.gui_top_graph.addLegend()
        self.top_plots = []

        # Sets the style for pyqtPlot top widget.
        self.gui_top_graph.setBackground('#32323C')
        self.top_legend.setLabelTextColor("#FFFFFF")
        self.gui_top_graph.getAxis('left').setPen(pg.mkPen(color='#FFFFFF'))
        self.gui_top_graph.getAxis('bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.gui_top_graph.getAxis("left").setTextPen((255, 255, 255))
        self.gui_top_graph.getAxis("bottom").setTextPen((255, 255, 255))

        # Set pyqtPlot lib to the bottom widget.
        self.gui_bottom_graph = pg.PlotWidget()
        self.gui_bottom_graph.getAxis("left").setTextPen((255, 255, 255))
        self.gui_bottom_graph.getAxis("bottom").setTextPen((255, 255, 255))
        self.gui_bottom_graph.getAxis('left').setPen(pg.mkPen(color='#FFFFFF'))
        self.gui_bottom_graph.getAxis(
            'bottom').setPen(pg.mkPen(color='#FFFFFF'))
        self.ui.gui_bottom_graph = qtw.QVBoxLayout()
        self.ui.bottom_widget.setLayout(self.ui.gui_bottom_graph)
        self.ui.gui_bottom_graph.addWidget(self.gui_bottom_graph)

        self.gui_bottom_graph.setBackground('#32323C')
        self.bottom_legend = self.gui_bottom_graph.addLegend()
        self.bottom_legend.setLabelTextColor("#FFFFFF")
        self.bottom_plots = []

        # Connect buttons to their function in event handler.
        # self.ui.projects.clicked.connect(__main__.eventHandler.launchProjects)
        self.ui.render.setDisabled(True)
        self.ui.help.clicked.connect(__main__.event_handler.help)
        self.ui.new_project.clicked.connect(__main__.event_handler.new_project)
        self.ui.upload.clicked.connect(__main__.event_handler.upload)
        self.ui.com_ports.activated[str].connect(
            __main__.event_handler.update_com)
        self.ui.disconnect.clicked.connect(
            __main__.event_handler.disconnect_device)
        self.ui.send.clicked.connect(
            __main__.event_handler.send_serial_input_to_device)
        self.ui.record.clicked.connect(__main__.event_handler.record)
        self.ui.lib_manager.clicked.connect(
            __main__.event_handler.launch_library)
        # self.ui.update.clicked.connect(__main__.eventHandler.update_warning)

        # Adds placeholder text
        self.ui.project_name.setPlaceholderText("Enter projct name here.")

        # Timings for repeating tasks such as getting data or updating graphs.
        timer = qtc.QTimer(self)
        timer.setInterval(15)
        timer.timeout.connect(self.update)
        timer.start()

    # One function that calls all other update functions
    def update(self):
        self.update_data()
        self.update_top_plot()
        self.update_bottom_plot()
        self.update_projects()
        self.update_com()
        self.blink_record()

        if __main__.data.errors >= 1:
            __main__.eventHandler.display_message()
            __main__.data.errors = 0

    # Updates the com ports drop down to all avaliable com ports
    def update_com(self):
        for serial_port in __main__.data.serial_ports():
            if serial_port not in [self.ui.com_ports.itemText(i) for i in range(self.ui.com_ports.count())]:
                self.ui.com_ports.addItem(serial_port)
        for serial_port in [self.ui.com_ports.itemText(i) for i in range(self.ui.com_ports.count())]:
            if serial_port not in __main__.data.serial_ports() and serial_port != "Select COM":
                target = self.ui.com_ports.findText(serial_port)
                self.ui.com_ports.removeItem(target)

    # Updates the current projects window so it shows all projects in the project folder.
    def update_projects(self):
        for project in __main__.fileManager.get_all_projects():
            if project not in [self.ui.project_paths.itemText(i) for i in range(self.ui.project_paths.count())]:
                self.ui.project_paths.addItem(project)
        for project in [self.ui.project_paths.itemText(i) for i in range(self.ui.project_paths.count())]:
            if project not in __main__.fileManager.get_all_projects():
                target = self.ui.project_paths.findText(project)
                self.ui.project_paths.removeItem(target)

    # Calls the main function to get all serial data
    def update_data(self):
        __main__.data.get_data()
        height_of_terminal = self.ui.centralwidget.height()
        __main__.data.number_of_lines_displayed_on_terminal = int(
            (height_of_terminal - 328) / 28)
        if not self.debug:
            self.ui.terminal.setHtml(__main__.data.html_terminal_text)

    def add_top_plots(self):
        for i in range(0, len(self.top_plots)):
            self.gui_top_graph.removeItem(self.top_plots[i])

        self.top_plots = []
        __main__.data.x_data = []
        __main__.data.top_plots_raw_data = []
        __main__.data.top_plots_data = []

        if len(__main__.data.labels[0]) > 0:
            for i in range(0, __main__.data.num_of_top_plots):

                pen = pg.mkPen("#FFFFFF", width=1)

                self.top_plots.append(self.gui_top_graph.plot(
                    [0], [0], name=__main__.data.labels[0][i], pen=pen))

    def add_bottom_plots(self):
        for i in range(0, len(self.bottom_plots)):
            self.gui_bottom_graph.removeItem(self.bottom_plots[i])

        self.bottom_plots = []
        __main__.data.x_data = []
        __main__.data.bottom_plots_raw_data = []
        __main__.data.bottom_plots_data = []

        if len(__main__.data.labels[1]) > 0:
            for i in range(0, __main__.data.num_of_bottom_plots):

                pen = pg.mkPen("#FFFFFF", width=1)

                self.bottom_plots.append(self.gui_bottom_graph.plot(
                    [0], [0], name=__main__.data.labels[1][i], pen=pen))

    def update_top_plot(self):
        if len(self.top_plots) != __main__.data.num_of_top_plots:
            self.add_top_plots()

        # Updates the Y axis data.
        try:
            for i in range(0, len(self.top_plots)):
                pen = pg.mkPen(
                    color=__main__.COLOUR_ORDER[i % len(__main__.COLOUR_ORDER)])
                self.top_plots[i].setData(
                    __main__.data.top_plots_data[i], pen=pen)
        except:
            pass

    def update_bottom_plot(self):
        if len(self.bottom_plots) != __main__.data.num_of_bottom_plots:
            self.add_bottom_plots()

        # Updates the Y axis data.
        try:
            for i in range(0, len(self.bottom_plots)):
                pen = pg.mkPen(
                    color=__main__.COLOUR_ORDER[i % len(__main__.COLOUR_ORDER)])
                self.bottom_plots[i].setData(
                    __main__.data.bottom_plots_data[i], pen=pen)
        except:
            pass

    def blink_record(self):
        self.i += 1
        if self.i % 75 == 0 and __main__.data.save_data:
            self.blink = not self.blink

            if self.blink:
                self.ui.record.setStyleSheet("""image: url(Ui/Record.png);
                                                image-position: left;
                                                padding-left: 10px;
                                                width: 10px""")
            else:
                self.ui.record.setStyleSheet("""""")
        elif self.i % 75 == 0 and not __main__.data.save_data:
            self.ui.record.setStyleSheet("""image: url(Ui/Record.png);
                                            image-position: left;
                                            padding-left: 10px;
                                            width: 10px""")
