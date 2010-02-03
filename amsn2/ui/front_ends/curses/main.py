
from amsn2.ui import base

import urwid
import sys

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core

    def show(self):
        palette = [
                ('bg', 'light gray', 'black'),
                ('label', 'yellow', 'light gray')]
        self._main = urwid.MainLoop(None, palette, unhandled_input=self.__handle_commands)
        self._amsn_core.idler_add(self.__on_show)

    def hide(self):
        raise urwid.ExitMainLoop()
        curses.nocbreak()
        self._stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def __on_show(self):
        self._amsn_core.main_window_shown()

    def set_title(self,title):
        self._title = title

    def set_menu(self,menu):
        pass

    def setFocusedWindow(self, window):
        self._command_line.setCharCb(window._on_char_cb)
        
    def __handle_commands(self, input):
        print >> sys.stderr, repr(input)
