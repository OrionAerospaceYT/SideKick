"""
A file to control the actuator testing suit on the
SideKick GUI.
"""


from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw

from Ui.ActuatorUi import Ui_MainWindow as actuator

class ActuatorGUI(qtw.QMainWindow):
    """
    a class
    """

    def __init__(self, device_manager, parent=None):

        super().__init__(parent=parent)

        self.actuators_ui = actuator()
        self.actuators_ui.setupUi(self)

        self.device_manager = device_manager

        self.actuators = {"select": None}

        self.pos = 0
        self.min = 0
        self.max = 90

        self.connect()

        timer = qtc.QTimer(self)
        timer.setInterval(25)
        timer.timeout.connect(self.update)
        timer.start()

        self.show()

    def connect(self):
        """
        Connects all widgets
        """

        self.actuators_ui.slider.setMinimum(self.min)
        self.actuators_ui.slider.setMaximum(self.max)
        self.actuators_ui.slider.setValue((self.min + self.max) // 2)
        self.actuators_ui.slider.setTickPosition(qtw.QSlider.TicksBelow)
        self.actuators_ui.slider.setTickInterval(self.max - self.min)
        self.actuators_ui.slider.valueChanged.connect(self.update_pos)

        self.actuators_ui.lower_lim.returnPressed.connect(self.set_lower_lim)
        self.actuators_ui.upper_lim.returnPressed.connect(self.set_upper_lim)

        self.actuators_ui.lower_lim.setText(str(self.min))
        self.actuators_ui.upper_lim.setText(str(self.max))

        self.actuators_ui.add_actuator.clicked.connect(self.add_new_actuator)

    def update_servos(self):
        """
        Updates all avaliable servos, removes unavaliable ones
        """
        servos_on_gui = [self.actuators_ui.select_actuator.itemText(
            i) for i in range(self.actuators_ui.select_actuator.count())]

        # adds new items
        for servo in self.actuators.keys():
            if servo not in servos_on_gui:
                self.actuators_ui.select_actuator.addItem(servo)

        # removes old items
        for servo in servos_on_gui:
            if servo not in self.actuators.keys():
                target = self.actuators_ui.select_actuator.findText(servo)
                self.actuators_ui.select_actuator.removeItem(target)

    def update(self):
        """
        Keeps all information relevant
        """

        self.actuators_ui.slider.setMinimum(self.min)
        self.actuators_ui.slider.setMaximum(self.max)

        try:
            self.actuators_ui.pos.setText(f"Position: {self.actuators_ui.slider.value()}")
            self.actuators_ui.actuator.setText(
                f"Actuator: {self.actuators_ui.select_actuator.currentText()}")
            self.actuators_ui.pin.setText(
                f"Pin: {self.actuators[self.actuators_ui.select_actuator.currentText()]}")
        except KeyError:
            pass

        self.update_servos()

    def update_pos(self):
        """
        Sends the message to the device.
        """
        indx = list(self.actuators.keys()).index(self.actuators_ui.select_actuator.currentText())
        self.device_manager.send(f"servo{indx-1}-{self.actuators_ui.slider.value()}")

    def set_upper_lim(self):
        """
        Sets the value of the upper limit
        """

        self.max = int(self.actuators_ui.upper_lim.text())

    def set_lower_lim(self):
        """
        Sets the value of the upper limit
        """

        self.min = int(self.actuators_ui.lower_lim.text())

    def add_new_actuator(self):
        """
        Defines a new actuator.
        """

        self.actuators[self.actuators_ui.name.text()] = int(self.actuators_ui.pin_input.text())
        self.device_manager.send(f"addservo-{int(self.actuators_ui.pin_input.text())}")

        self.actuators_ui.name.setText("")
        self.actuators_ui.pin_input.setText("")
