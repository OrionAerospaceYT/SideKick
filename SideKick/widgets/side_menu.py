"""
The side menu class
"""

class SideMenu:
    """
    A class to control showing and hiding menus.

    Attributes:
        widgets_file (list): a list of widgets for the file side menu
        widgets_device (list): a list of widgets for the device side menu
        layout (pyqt layout): the layout that holds both side menus
        showing_file (bool): whether the file widgets are being shown
        showing_device (bool): whether the device widgets are being shown
    
    Methods:
        show_side_menu:
            Updates the side menu to show the correct one.

            Args:
                file (bool) whether to update file being displayed
                device (bool) whether to update device being displayed
        
        hide_menu:
            Hides the entire display (used on startup).
    """

    def __init__(self, widgets_file, widgets_device, layout):

        self.widgets_file = widgets_file
        self.widgets_device = widgets_device
        self.layout = layout

        self.showing_file = False
        self.showing_device = False

    def show_side_menu(self, file=False, device=False):
        """
        Updates the side menu to show the correct one.

        Args:
            file (bool) whether to update file being displayed
            device (bool) whether to update device being displayed
        """
        if file:
            self.showing_file = not self.showing_file
            self.showing_device = False
        elif device:
            self.showing_device = not self.showing_device
            self.showing_file = False

        if self.showing_device:
            self.widgets_file.setVisible(self.showing_file)
            self.widgets_device.setVisible(self.showing_device)
        elif self.showing_file:
            self.widgets_device.setVisible(self.showing_device)
            self.widgets_file.setVisible(self.showing_file)

        self.layout.setVisible(
            self.showing_file or self.showing_device)

    def hide_menu(self):
        """
        Hides the entire display (used on startup).
        """
        self.layout.setVisible(False)
