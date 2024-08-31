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

    def setUp(self):
        self.gui = MainGUI()

if __name__ == "__main__":
    unittest.main()