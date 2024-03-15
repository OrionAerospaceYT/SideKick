"""
A file to control the actuator testing suit on the
SideKick GUI.
"""


from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg

from Ui.ActuatorUi import Ui_MainWindow as actuator

class Slider:
    """
    Creates sliders for the actuator test window.
    """
    def __init__(self, name, minimum, maximum, actuator_type):

        self.actuator_type = actuator_type

        mid_point = (minimum + maximum) // 2

        self.horizontal_layout = qtw.QHBoxLayout()

        name_label = qtw.QLabel(name)
        name_label.setMinimumWidth(100)
        name_label.setMinimumHeight(50)

        self.slider = qtw.QSlider()
        self.slider.setOrientation(qtc.Qt.Horizontal)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setValue(mid_point)

        self.pos_label = qtw.QLabel().setText(str(mid_point))

        spacer = qtw.QSpacerItem(20,
                                40,
                                qtw.QSizePolicy.Minimum,
                                qtw.QSizePolicy.Maximum)

        self.horizontal_layout.addWidget(name_label)
        self.horizontal_layout.addWidget(self.slider)
        self.horizontal_layout.addWidget(self.pos_label)
        self.horizontal_layout.addItem(spacer)


class ActuatorGUI(qtw.QMainWindow):
    """
    A class to show and control the test actuator window
    """

    def __init__(self, device_manager, parent=None):

        self.parent = parent

        super().__init__(parent=self.parent)

        self.actuators_ui = actuator()
        self.actuators_ui.setupUi(self)

        self.actuators = {"pins" : {}, "servos" : {}}
        self.sliders = {"pins" : [], "servos" : []}

        self.device_manager = device_manager

        self.restart = True

        print(parent.file_manager.get_examples())

        self()

        timer = qtc.QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self)
        timer.start()

    def __call__(self):

        if not self.restart:
            return

        self.device_manager.send("reset")

        self.clear_layout(self.actuators_ui.verticalLayout_2)

        self.actuators = {"pins" : {}, "servos" : {}}
        self.sliders = {"pins" : [], "servos" : []}

        self.restart = False

        self.set_place_holder_text()

        self.actuators_ui.progressBar.setMinimum(0)
        self.actuators_ui.progressBar.setMaximum(0)

        self.actuators_ui.loading.setVisible(False)

        self.actuators_ui.add.clicked.connect(self.add_new_actuator)
        self.actuators_ui.upload.clicked.connect(self.upload)

        upload = qtw.QShortcut(qtg.QKeySequence("ctrl+u"), self)
        upload.activated.connect(self.upload)

        self.actuators_ui.value.setMinimum(0)
        self.actuators_ui.value.setValue(50)
        self.actuators_ui.value.setMaximum(100)

        self.actuators_ui.value.valueChanged.connect(lambda: self.update_pos_all(
                self.actuators_ui.value.value()))

        self.restart = False

    def clear_layout(self, layout):
        """
        Removes all layouts and widgets from the screen except for first item.
        """
        while layout.count() > 1:
            child = layout.takeAt(1)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_sub_layout(child.layout())

    def clear_sub_layout(self, layout):
        """
        Removes all layouts and widgets from the screen.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def set_place_holder_text(self):
        """
        Sets all of the place holder text for the line edits on
        the window
        """
        self.actuators_ui.name.setPlaceholderText("Name")
        self.actuators_ui.pin.setPlaceholderText("Pin")
        self.actuators_ui.min.setPlaceholderText("Minimum")
        self.actuators_ui.max.setPlaceholderText("Maximum")

    def set_progress(self, value):
        """
        Sets the progress value on the progress bar

        Args:
            value (int): the percentage of the way through
        """
        self.actuators_ui.progressBar.setValue(value)

    def upload(self):
        """
        Uploads the actuator test demo.
        """
        self.parent.upload_project(actuator=True)
        self.actuators_ui.scrollArea.setVisible(False)
        self.actuators_ui.options_widget.setVisible(False)
        self.actuators_ui.loading.setVisible(True)

    def done_upload(self):
        """
        Removes inputs while uploading so the user does not miss
        assigning any actuators.
        This functions puts them back on once the upload is complete.
        """
        self.actuators_ui.scrollArea.setVisible(True)
        self.actuators_ui.options_widget.setVisible(True)
        self.actuators_ui.loading.setVisible(False)
        self.restart = True

    def update_pos(self, value, indx, actuator_type):
        """
        Sends the message to the device.
        
        Args:
            value (int): the position to move the actuator
            indx (int): the number of the actuator to move
        """
        if actuator_type == "Servo":
            self.device_manager.send(f"servo{indx}-{value}")
            print(f"servo{indx}-{value}")
        elif actuator_type == "Pin":
            print(f"pin{indx}-{value}")
            self.device_manager.send(f"pin{indx}-{value}")

    def update_pos_all(self, value):
        """ 
        Sends string to device for every actuator in the actuator list.

        Args:
            value (int): the percentage to move the actuator
        """
        value /= 100

        for i, key in enumerate(self.actuators["servos"].items()):
            position = int(key[1][1] + (key[1][2] - key[1][1]) * value)
            self.device_manager.send(f"servo{i}-{position}")

        for i, key in enumerate(self.actuators["pins"].items()):
            position = int(key[1][1] + (key[1][2] - key[1][1]) * value)
            self.device_manager.send(f"pin{i}-{position}")

    def create_new_slider(self, name, minimum, maximum, actuator_type):
        """
        Creates the layout for a new slider.
        """

        slider = Slider(name, minimum, maximum, actuator_type)

        if actuator_type == "Servo":
            slider.slider.valueChanged.connect(lambda: self.update_pos(slider.slider.value(),
                                            self.sliders["servos"].index(slider.horizontal_layout),
                                            actuator_type))

        elif actuator_type == "Pin":
            slider.slider.valueChanged.connect(lambda: self.update_pos(slider.slider.value(),
                                            self.sliders["pins"].index(slider.horizontal_layout),
                                            actuator_type))

        return slider

    def add_new_actuator(self):
        """
        Defines a new actuator.
        """
        name = self.actuators_ui.name.text()
        actuator_type = self.actuators_ui.type.currentText()

        try:
            pin = int(self.actuators_ui.pin.text().strip())
            minimum = int(self.actuators_ui.min.text().strip())
            maximum = int(self.actuators_ui.max.text().strip())
        except ValueError:
            print("<<< WARNING >>> PIN, MIN, MAX NEED TO BE INTEGERS")
            return

        if actuator_type == "Servo":
            self.actuators["servos"][name] = [pin, minimum, maximum]

            self.device_manager.send(f"addServo-{pin}")

            slider = self.create_new_slider(name, minimum, maximum, actuator_type)
            self.sliders["servos"].append(slider.horizontal_layout)
            self.actuators_ui.verticalLayout_2.addLayout(self.sliders["servos"][-1])

        elif actuator_type == "Pin":
            self.actuators["pins"][name] = [pin, minimum, maximum]

            self.device_manager.send(f"addPin-{pin}")

            slider = self.create_new_slider(name, minimum, maximum, actuator_type)
            self.sliders["pins"].append(slider.horizontal_layout)
            self.actuators_ui.verticalLayout_2.addLayout(self.sliders["pins"][-1])

        self.actuators_ui.name.setText("")
        self.actuators_ui.pin.setText("")
        self.actuators_ui.min.setText("")
        self.actuators_ui.max.setText("")
