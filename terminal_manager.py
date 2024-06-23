import copy
from PyQt5.QtGui import QTextCursor, QTextDocumentFragment, QTextBlockFormat

class Terminal():

    def __init__(self, text_edit, data_stream):
        self.text_edit = text_edit
        self.data_stream = data_stream
        self.prev_scroll_pos = None

    def compile_batch(self):
        # Compile the batch into a correctly formatted string
        new_data = copy.deepcopy(self.data_stream.data)
        self.data_stream.data = self.data_stream.data[len(new_data):]
        msg_format = "<span style=\"color:#00f0c3;\">>>></span>{}"
        batch = " "
        for item in reversed(new_data):
            batch += msg_format.format(item)
        if batch.endswith("<br>"):
            batch = batch[:-4]
        fragment = QTextDocumentFragment.fromHtml(batch)
        return fragment

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
        for _ in range(self.text_edit.document().blockCount() - 10000):
            cursor.movePosition(cursor.PreviousBlock, cursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.deleteChar()

    def update_text(self):
        # Check if there is any new data to write
        if not self.data_stream.data:
            return

        # Save the current scroll positions
        scroll_bar = self.text_edit.verticalScrollBar()
        current_scroll_pos = scroll_bar.value()
        max_scroll_pos = scroll_bar.maximum()

        # Save the cursor position
        cursor = self.text_edit.textCursor()
        saved_cursor_position = cursor.position()

        # Update the text
        fragment = self.compile_batch()
        self.write_text(fragment)
        self.limit_line_count()

        # Restore the cursor position
        cursor.setPosition(saved_cursor_position)
        self.text_edit.setTextCursor(cursor)

        # Restore the scroll position relative to the maximum value
        if current_scroll_pos > 20:
            new_max_scroll_pos = scroll_bar.maximum()
            new_scroll_pos = new_max_scroll_pos - (max_scroll_pos - current_scroll_pos)
            scroll_bar.setValue(new_scroll_pos)
