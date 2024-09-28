"""
The sidekick lite class
"""

from SideKick.globals import SK_LITE_OFF_QSS, SK_LITE_ON_QSS

class SideKickLite:
    """
    Converts the sidekick lite button to a checkbox
    """

    def __init__(self, widget, startup_state):
        self.state = startup_state
        self.button = widget
        self.button.clicked.connect(self.update_state)

        self.update_style_sheet()

    def update_state(self):
        """
        Changes the boolean state variable and updates the stylesheet.
        """
        self.state = not self.state
        self.update_style_sheet()

    def update_style_sheet(self):
        """
        Sets the stylesheet to the correct type for the state.
        """
        if self.state:
            self.button.setStyleSheet(SK_LITE_ON_QSS)
            self.button.setText("SideKick Lite: ON")
        else:
            self.button.setStyleSheet(SK_LITE_OFF_QSS)
            self.button.setText("SideKick Lite: OFF")
