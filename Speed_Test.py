import sys
import time
import random
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor, QTextDocumentFragment, QTextBlockFormat

RUNNING = True

class FakeData():
    def __init__(self):
        self.data = []

    def append_data(self):
        while RUNNING:
            new_string = "New value: " + str(random.randint(0,10)) + "\n"
            #print(new_string)
            self.data.append(new_string)
            time.sleep(0.01)

class RealTimeTextDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
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
        if not my_data.data:
            return

        msg_format = "<span style=\"color:#00f0c3;\">>>></span>{}"
        batch = " "
        for item in reversed(my_data.data):
            batch += msg_format.format(item.replace("\n", "<br>"))
        fragment = QTextDocumentFragment.fromHtml(batch)

        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.insertFragment(fragment)
        block_format = QTextBlockFormat()
        block_format.setLineHeight(5, QTextBlockFormat.FixedHeight)
        cursor.insertBlock(block_format)
        my_data.data=[]

        # Limit the number of lines in the QTextEdit
        cursor = self.text_edit.textCursor()
        scroll_pos = self.text_edit.verticalScrollBar().value()

        cursor.movePosition(cursor.End)
        print(self.text_edit.document().blockCount())
        for _ in range(self.text_edit.document().blockCount() - 2000):
            cursor.movePosition(cursor.PreviousBlock, cursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.deleteChar()

        self.text_edit.setTextCursor(cursor)
        self.text_edit.verticalScrollBar().setValue(scroll_pos)

if __name__ == '__main__':
    my_data = FakeData()

    app = QApplication(sys.argv)
    ex = RealTimeTextDisplay()
    ex.show()
    data = threading.Thread(target=my_data.append_data)
    data.start()
    sys.exit(app.exec_())
    RUNNING = False
