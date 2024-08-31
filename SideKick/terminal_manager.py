"""
To speed up the GUI, the terminal is written to in batches and class terminal deals with managing
the terminal and displaying information on it. The terminal is styled using HTML syntax.
"""
import re
import copy

from PyQt6 import QtGui as qtg

from SideKick.globals import GRAPH_BEGINNING, GRAPH_ENDING, NUM_OF_DATA_PTS

class Terminal():
    """
    Handles the terminal data and widget to show the inputs from the hardware to the user.

    Attributes:
        text_edit(QTextEdit): the terminal widget
        data_stream(list): all of the data which is still to be written to the terminal 
        prev_scroll_pos(int): the last position of the scroll bar
        running_average(list): a list of the lengths of every block of data written to the terminal

    Methods:
        TODO
    """
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.text_edit.setReadOnly(True)

        self.data_stream = []
        self.prev_scroll_pos = None

        self.running_average = []

    def append_data(self, raw_data):
        """
        Append the new data to the data stream.

        Args:
            raw_data(list): all of the new input items from the device
        """
        for item in raw_data:
            self.data_stream.append(item)

    def compile_batch(self):
        """
        Compile the batch into a correctly formatted string.
        """
        batch = ""
        msg_format = "<span style=\"color:#00f0c3;\">&> </span>{}"
        new_data = copy.deepcopy(self.data_stream)
        length = len(new_data)-1
        self.data_stream = self.data_stream[len(new_data):]

        for i, item in enumerate(reversed(new_data)):
            msg = re.sub(f'{GRAPH_BEGINNING}.*?{GRAPH_ENDING}', '', item)
            if not msg:
                continue
            batch += msg_format.format(msg)
            if i != length:
                batch += "<br>"

        self.running_average.append(length)

        return batch

    def write_text(self, fragment):
        """
        Create the cursor and write the data to the screen
        """
        cursor = self.text_edit.textCursor()
        block_format = qtg.QTextBlockFormat()
        block_format.setBottomMargin(0)

        cursor.movePosition(qtg.QTextCursor.MoveOperation.Start)
        cursor.insertBlock(block_format)
        cursor.insertFragment(fragment)

    def limit_line_count(self):
        """
        Limit the number of lines in the QTextEdit
        """
        num_of_blocks = self.text_edit.document().blockCount()
        cursor = self.text_edit.textCursor()
        cursor.movePosition(qtg.QTextCursor.MoveOperation.End)
        for _ in range(num_of_blocks - self.calculate_num_of_blocks()):
            cursor.movePosition(
                qtg.QTextCursor.MoveOperation.PreviousBlock, qtg.QTextCursor.MoveMode.KeepAnchor)
        self.running_average = self.running_average[num_of_blocks:]
        cursor.removeSelectedText()
        cursor.deleteChar()

    def calculate_num_of_blocks(self):
        """
        Calculates the average number of lines
        """
        return int(NUM_OF_DATA_PTS * len(self.running_average) / (sum(self.running_average) + 1))

    def update_text(self):
        """
        Adds the new block of data to the terminal and maintains scrolling on the same data
        that the user was looking at prior to the new data being added
        """
        if not self.data_stream:
            return

        # Save the current scroll positions
        scroll_bar = self.text_edit.verticalScrollBar()
        current_scroll_pos = scroll_bar.value()
        max_scroll_pos = scroll_bar.maximum()

        # Save the cursor position
        cursor = self.text_edit.textCursor()
        saved_cursor_position = cursor.position()

        # Update the text
        batch = self.compile_batch()
        if not batch:
            return
        fragment = qtg.QTextDocumentFragment.fromHtml(batch)
        self.write_text(fragment)

        # Restore the cursor position
        cursor.setPosition(saved_cursor_position)
        self.text_edit.setTextCursor(cursor)

        # Restore the scroll position relative to the maximum value
        if current_scroll_pos > 100:
            new_max_scroll_pos = scroll_bar.maximum()
            new_scroll_pos = new_max_scroll_pos - (max_scroll_pos - current_scroll_pos)
            scroll_bar.setValue(new_scroll_pos)
            if new_scroll_pos > scroll_bar.value():
                scroll_bar.setValue(0)

        self.limit_line_count()

    def clear(self):
        """
        Clear all of the text from the temrinal widget
        """
        self.text_edit.setText("")
