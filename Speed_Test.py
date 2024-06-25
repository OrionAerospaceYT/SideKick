import sys
import time
import copy
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor, QTextDocumentFragment, QTextBlockFormat

from terminal_manager import Terminal

RUNNING = True

class FakeData():
    def __init__(self):
        self.data = []
        self.counter = 0

    def append_data(self):
        while RUNNING:
            self.counter += 1
            new_string = "This is a very long example with a new value: " + str(self.counter) + "<br>"
            #print(new_string)
            ex.terminal.append_data([new_string])
            time.sleep(0.01)

class RealTimeTextDisplay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        
        self.terminal = Terminal(self.text_edit)

        # Set up a timer to update the text periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(0)  # Update every second

    def initUI(self):
        self.setWindowTitle('Real-Time Text Display')
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
    def update_text(self):
        self.terminal.update_text()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = RealTimeTextDisplay()
    my_data = FakeData()
    ex.show()
    data = threading.Thread(target=my_data.append_data)
    data.start()
    app.exec_()
    RUNNING = False
    print("ENDED")
