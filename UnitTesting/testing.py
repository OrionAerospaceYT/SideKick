"""
Testing
"""
import os
import sys
import time
import unittest

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

parent = os.path.abspath('.')
sys.path.insert(1, parent)

from main import MainGUI

app = qtw.QApplication(sys.argv)
gui = MainGUI()

class TestGui(unittest.TestCase):
    """
    Testing the main features and backend of the SideKickGUI.
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

    def test_verify_install(self):
        """
        Verifies the installation of the SideKick GUI.
        """
        print(gui.main_ui.com_ports.currentText())
        self.assertEqual(gui.main_ui.bottom_update.text(), "Not Connected")
        self.assertEqual(0,1)

if __name__ == "__main__":
    unittest.main()
