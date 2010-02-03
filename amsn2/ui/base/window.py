
class aMSNWindow(object):
    """ This Interface represents a window of the application. Everything will be done from here """
    def __init__(self, amsn_core):
        """
        @type amsn_core: aMSNCore
        """

        raise NotImplementedError

    def show(self):
        """ This launches the window, creates it, etc.."""
        raise NotImplementedError

    def hide(self):
        """ This should hide the window"""
        raise NotImplementedError

    def set_title(self, text):
        """
        This will allow the core to change the current window's title

        @type text: str
        """
        raise NotImplementedError

    def set_menu(self, menu):
        """
        This will allow the core to change the current window's main menu

        @type menu: MenuView
        """
        raise NotImplementedError
