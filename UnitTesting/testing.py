"""
Testing
"""
import os
import sys
import unittest

parent = os.path.abspath('.')
sys.path.insert(1, parent)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest

from main import MainGUI

app = QApplication(sys.argv)

class SideKickGuiTester(unittest.TestCase):
    """
    Testing the main features and backend of the SideKickGUI.
    """

    def setUp(self, test_gui):
        self.gui = test_gui

    def testing_tests(self):
        self.assertEqual(0,0)

if __name__ == "__main__":

    test_gui = MainGUI()
    unittest.main(test_gui)
    test_gui.close_gui()
