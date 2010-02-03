
class aMSNMainWindow(object):
    """ This Interface represents the main window of the application. Everything will be done from here 
    When the window is shown, it should call: amsn_core.mainWindowShown()
    When the user wants to close that window, amsn_core.quit() should be called.
    """

    def __init__(self, amsn_core):
        """
        @type amsn_core: aMSNCore
        """

        pass

    def show(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def set_title(self,title):
        raise NotImplementedError

    def set_menu(self,menu):
        raise NotImplementedError

