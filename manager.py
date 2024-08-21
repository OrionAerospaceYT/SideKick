"""
A wrapper file for the board and library manager classes as they overlap with their
setup.
"""
import webbrowser

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from Ui.ManagerUi import Ui_MainWindow as manager

from globals import SELECTED_WIDGET_QSS, NORMAL_WIDGET_QSS

def library_no_results():
    """
    Create a QTextBrowser to show the user that there are no results
    """
    no_results = qtw.QTextBrowser()
    no_results.setHtml("""
<h2><p style="color:#00f0c3">No results found!</p></h2><br>
<p>Please check your spelling or try another search term.</p><br>
""")
    return no_results

def library_instructions():
    """
    Create a QTextBrowser to explain to the user how to use the library manager
    """
    instructions = qtw.QTextBrowser()
    instructions.setHtml("""
<h2><p style="color:#00f0c3">Search for your library!</p></h2><br>
<p>Please enter a key word or phrase of the library you are looking
for which is at least three characters long.</p>
""")
    return instructions

class ManagerWidget(qtw.QTextBrowser):
    """
    Testing
    """
    def __init__(self, name, versions, html, index, parent=None):
        self.name = name
        self.index = index
        self.parent = parent
        self.versions = versions

        super().__init__(parent)

        self.setHtml(html)
        self.setTextInteractionFlags(qtc.Qt.LinksAccessibleByMouse | qtc.Qt.NoTextInteraction)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        document = self.document()
        document.adjustSize()
        scale = max(self.parent.file_manager.get_scale() * 1.7, 0.7*1.7)
        self.setMinimumHeight(int(document.size().height()*scale))

        self.anchorClicked.connect(self.handle_anchor_clicked)

    def handle_anchor_clicked(self, url):
        """
        Open the URL in the default web browser.
        """
        html = self.toHtml()
        webbrowser.open(url.toString())
        self.setHtml(html)

    def mousePressEvent(self, event):
        """
        Adds an event if the QTextBrowser is clicked.
        """
        if event.button() == qtc.Qt.LeftButton:
            self.parent.update_selected(self.index)
        super().mousePressEvent(event)

class Manager(qtw.QMainWindow):
    """
    A wrapper class for both the library and boards manager windows so as to not
    write duplicate code.
    """

    def __init__(self, window_title:str, manager_type:str, searchable=False, parent=None):
        super().__init__(parent=parent)
        self.manager_ui = manager()

        # Definition of attributes
        self.parent = parent
        self.file_manager = self.parent.file_manager
        self.cli_manager = self.parent.cli_manager

        self.widgets = []
        self.selected = -1

        self.searchable = searchable
        self.window_title = window_title
        self.manager_type = manager_type

        self.setup_window()

    def setup_window(self):
        """
        Set the size of the window and the different texts that are displayed
        """
        self.manager_ui.setupUi(self)

        self.setWindowTitle(self.window_title)
        self.resize(int(self.parent.width()*0.8), int(self.parent.height()*0.8))
        self.setWindowModality(2)

        self.manager_ui.install.setText(f"Select a {self.manager_type} to install")

        if not self.searchable:
            self.manager_ui.search_bar.setVisible(False)

    def clear_widgets(self):
        """
        Removes all of the widgets in the scroll area
        """
        while self.manager_ui.selectable_items.count():
            child = self.manager_ui.selectable_items.takeAt(0)
            child.widget().deleteLater()

        self.widgets = []
        self.update_selected(-1)

    def add_widget(self, name:str, widget_dictionary:dict):
        """
        Update the widgets which are shown in the QScrollArea
        """

        versions = self.file_manager.get_versions(name, widget_dictionary)
        html = self.file_manager.get_html(name, widget_dictionary)

        self.widgets.append(ManagerWidget(name, versions, html, len(self.widgets), self))
        self.manager_ui.selectable_items.addWidget(self.widgets[-1])

    def update_selected(self, index:int):
        """
        Update the selected library and if the one which is already selected is clicked then
        set selected to -1 as it is an impossible index otherwise
        """
        while self.manager_ui.versions.currentText():
            self.manager_ui.versions.removeItem(0)

        self.manager_ui.install.setText(f"Select a {self.manager_type} to install")

        # Set the previous widget back to normal
        if self.selected != -1:
            self.widgets[self.selected].setStyleSheet(NORMAL_WIDGET_QSS)

        # Update the selected index
        if index == self.selected:
            self.selected = -1
        else:
            self.selected = index

        # Set the new widget to have the selected stylesheet
        if self.selected != -1:
            self.widgets[self.selected].setStyleSheet(SELECTED_WIDGET_QSS)
            self.manager_ui.install.setText("Install: " + self.widgets[self.selected].name)
            for item in self.widgets[self.selected].versions:
                self.manager_ui.versions.addItem(item)

        if not self.manager_ui.versions.currentText():
            self.manager_ui.versions.addItem("N/A")
