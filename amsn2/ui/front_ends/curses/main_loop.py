
from amsn2.ui import base
import gobject
import urwid

gobject.threads_init()

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        palette = [
                ('bg', 'light gray', 'black'),
                ('label', 'yellow', 'dark blue')]
        frame = urwid.Frame(urwid.Filler(urwid.Text("aMSN2")),header=urwid.Text("Welcome to aMSN2"),footer=urwid.Text("(cmd)"))
        self._main = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())
        self._mainloop = self._main.event_loop

    def run(self):
        self._main.run()

    def idler_add(self, func):
        gobject.idle_add(func)

    def timer_add(self, delay, func):
        gobject.timeout_add(delay, func)

    def quit(self):
        raise urwid.ExitMainLoop()

