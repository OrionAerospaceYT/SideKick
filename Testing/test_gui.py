"""
Test the setup and run of the GUI as a whole system seperate from unittesting
"""
import os
import sys
import unittest

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

parent = os.path.abspath('.')
sys.path.insert(1, parent)

from main import MainGUI

app = qtw.QApplication(sys.argv)
gui = MainGUI()

INSTALLED_BOARDS = [
"Select Board",
"SK Stem",
"Adafruit Circuit Playground",
"Arduino BT",
"Arduino Duemilanove or Diecimila arduino:avr:diecimila",
"Arduino Esplora",
"Arduino Ethernet",
"Arduino Fio",
"Arduino Gemma",
"Arduino Industrial 101",
"Arduino Leonardo",
"Arduino Leonardo ETH",
"Arduino Mega ADK",
"Arduino Mega or Mega 2560",
"Arduino Micro",
"Arduino Mini",
"Arduino NG or older",
"Arduino Nano",
"Arduino Pro or Pro Mini",
"Arduino Robot Control",
"Arduino Robot Motor",
"Arduino Uno",
"Arduino Uno Mini",
"Arduino Uno WiFi",
"Arduino Yún",
"Arduino Yún Mini",
"LilyPad Arduino",
"LilyPad Arduino USB",
"Linino One",
"Raspberry Pi Pico",
"Teensy 2.0",
"Teensy 3.0",
"Teensy 3.2 / 3.1",
"Teensy 3.5",
"Teensy 3.6",
"Teensy 4.0",
"Teensy 4.1",
"Teensy LC",
"Teensy MicroMod",
"Teensy++ 2.0"
]

class TestGui(unittest.TestCase):
    """
    Testing the main features and backend of the SideKickGUI in an integration test
    """

    @classmethod
    def setUpClass(cls):
        print("Setting up the tests...")
        app.setWindowIcon(qtg.QIcon("Ui/SideKick.ico"))
        gui.show()
        app.processEvents()
        print("Done.")

    @classmethod
    def tearDownClass(cls):
        print("Closing SideKick GUI...")
        app.closeAllWindows()
        gui.close_gui()
        print("Done.")

    def test_running_gui(self):
        """
        Verifies the installation of the SideKick GUI
        """
        app.processEvents()
        self.assertEqual(0, 0)

    def test_check_installed_boards(self):
        """
        Check that all of the correct boards have been installed
        """
        boards = []
        for i in range(gui.main_ui.supported_boards.count()):
            print(gui.main_ui.supported_boards.itemText(i))
            boards.append(gui.main_ui.supported_boards.itemText(i))
        self.assertEqual(boards, INSTALLED_BOARDS)

    def test_check_connection_status(self):
        """
        As there is no device to connect to, check the Connected status is not connected
        """
        self.assertEqual(gui.main_ui.bottom_update.text(), "Not Connected")

if __name__ == "__main__":
    # Run the integration test
    unittest.main()
