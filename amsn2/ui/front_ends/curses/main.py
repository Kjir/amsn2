
from amsn2.ui import base

import urwid
import sys

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core

    def show(self):
        self._main = self._amsn_core._loop._main
        self._main.unhandled_input = self.__handle_commands
        self._amsn_core.idler_add(self.__on_show)

    def hide(self):
        raise urwid.ExitMainLoop()

    def __on_show(self):
        self._amsn_core.main_window_shown()

    def set_title(self,title):
        self._main.set_header = urwid.Text(title)

    def set_menu(self,menu):
        pass

    def setFocusedWindow(self, window):
        self._command_line.setCharCb(window._on_char_cb)
        
    def __handle_commands(self, input):
        print >> sys.stderr, repr(input)
