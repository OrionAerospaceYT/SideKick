import re
import copy

from PyQt5.QtGui import QTextDocumentFragment, QTextBlockFormat

from globals import GRAPH_BEGINNING, GRAPH_ENDING

class Terminal():

    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.text_edit.setReadOnly(True)

        self.data_stream = []
        self.prev_scroll_pos = None

    def append_data(self, raw_data):
        # Append the new data to the data stream
        for item in raw_data:
            self.data_stream.append(item)

    def compile_batch(self):
        # Compile the batch into a correctly formatted string
        new_data = copy.deepcopy(self.data_stream)
        self.data_stream = self.data_stream[len(new_data):]
        msg_format = "<span style=\"color:#00f0c3;\">>>></span>{}"
        batch = " "
        for item in reversed(new_data):
            msg = re.sub(f'{GRAPH_BEGINNING}.*?{GRAPH_ENDING}', '', item)
            if not msg:
                continue
            batch += msg_format.format(msg)
            batch += "<br>"
        if batch.endswith("<br>"):
            batch = batch[:-4]
        print("New Batch")
        print(repr(batch))
        return batch

    def write_text(self, fragment):
         # Create the cursor and write the data to the screen
        cursor = self.text_edit.textCursor()
        block_format = QTextBlockFormat()
        block_format.setBottomMargin(0)

        cursor.movePosition(cursor.Start)
        cursor.insertBlock(block_format)
        cursor.insertFragment(fragment)

    def limit_line_count(self):
        # Limit the number of lines in the QTextEdit
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.End)
        for _ in range(self.text_edit.document().blockCount() - 500):
            cursor.movePosition(cursor.PreviousBlock, cursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.deleteChar()

    def update_text(self):
        # Check if there is any new data to write
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
        fragment = QTextDocumentFragment.fromHtml(batch)
        self.write_text(fragment)

        # Restore the cursor position
        cursor.setPosition(saved_cursor_position)
        self.text_edit.setTextCursor(cursor)

        # Restore the scroll position relative to the maximum value
        if current_scroll_pos > 20:
            new_max_scroll_pos = scroll_bar.maximum()
            new_scroll_pos = new_max_scroll_pos - (max_scroll_pos - current_scroll_pos)
            scroll_bar.setValue(new_scroll_pos)

        self.limit_line_count()

    def clear(self):
        self.text_edit.setText("")