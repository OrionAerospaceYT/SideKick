"""
A file to control the actuator testing suit on the
SideKick GUI.
"""


from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from Ui.NewActuatorUi import Ui_MainWindow as actuator

class Slider:
    """
    Creates sliders for the actuator test window.
    """
    def __init__(self, name, minimum, maximum, parent=None):
        mid_point = (minimum + maximum) // 2

        self.horizontal_layout = qtw.QHBoxLayout()

        self.name_label = qtw.QLabel(name)

        self.slider = qtw.QSlider(parent)
        self.slider.setOrientation(qtc.Qt.Horizontal)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(mid_point)

        self.pos_label = qtw.QLabel().setText(str(mid_point))

        spacer = qtw.QSpacerItem(20,
                                40,
                                qtw.QSizePolicy.Minimum,
                                qtw.QSizePolicy.Maximum)

        self.horizontal_layout.addWidget(self.name_label)
        self.horizontal_layout.addWidget(self.slider)
        self.horizontal_layout.addWidget(self.pos_label)
        self.horizontal_layout.addItem(spacer)


class ActuatorGUI(qtw.QMainWindow):
    """
    A class to show and control the test actuator window
    """

    def __init__(self, device_manager, parent=None):

        super().__init__(parent=parent)

        self.actuators_ui = actuator()
        self.actuators_ui.setupUi(self)

        self.device_manager = device_manager

        self.actuators = {"All Actuators": 0}

        self.sliders = []

        self.done = False

        self.set_place_holder_text()

        self.actuators_ui.progressBar.setMinimum(0)
        self.actuators_ui.progressBar.setMaximum(0)

        self.actuators_ui.scrollArea.setVisible(False)
        self.actuators_ui.options_widget.setVisible(False)

        self.actuators_ui.add.clicked.connect(self.add_new_actuator)

        self.show()

        self.timer = qtc.QTimer(self)
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.display_all)
        self.timer.start()

    def set_place_holder_text(self):
        """
        Sets all of the place holder text for the line edits on
        the window
        """
        self.actuators_ui.name.setPlaceholderText("Name")
        self.actuators_ui.pin.setPlaceholderText("Pin")
        self.actuators_ui.min.setPlaceholderText("Minimum")
        self.actuators_ui.max.setPlaceholderText("Maximum")

    def set_done_upload(self):
        """
        Sends the command to stop loading and show scroll bars
        """
        self.done = True

    def display_all(self):
        """
        Stops loading and shows scroll bars
        """
        if not self.done:
            return

        self.actuators_ui.loading.setVisible(False)
        self.actuators_ui.scrollArea.setVisible(True)
        self.actuators_ui.options_widget.setVisible(True)
        self.timer.stop()

    def set_progress(self, value):
        """
        Sets the progress value on the progress bar

        Args:
            value (int): the percentage of the way through
        """
        self.actuators_ui.progressBar.setValue(value)

    def update_pos(self, value, indx):
        """``
        Sends the message to the device.
        """
        self.device_manager.send(f"servo{indx}-{value}")
        #self.sliders[indx].pos_label.setText(str(value))

    def create_new_slider(self, name, minimum, maximum):
        """
        Creates the layout for a new slider.
        """

        slider = Slider(name, minimum, maximum, self.actuators_ui.scrollAreaWidgetContents)
        slider.slider.valueChanged.connect(lambda: self.update_pos(slider.slider.value(),
                                            self.sliders.index(slider.horizontal_layout)))
        return slider

    def add_new_actuator(self):
        """
        Defines a new actuator.
        """
        name = self.actuators_ui.name.text()

        try:
            pin = int(self.actuators_ui.pin.text())
            minimum = int(self.actuators_ui.min.text())
            maximum = int(self.actuators_ui.max.text())
        except ValueError:
            print("<<< WARNING >>> PIN, MIN, MAX NEED TO BE INTEGERS")
            return

        self.actuators[name] = [pin, minimum, maximum]
        self.device_manager.send(f"addservo-{pin}")

        slider = self.create_new_slider(name, minimum, maximum)
        self.sliders.append(slider.horizontal_layout)
        self.actuators_ui.verticalLayout_2.addLayout(self.sliders[-1])

        self.actuators_ui.name.setText("")
        self.actuators_ui.pin.setText("")
        self.actuators_ui.min.setText("")
        self.actuators_ui.max.setText("")
