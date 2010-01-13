from __future__ import with_statement
from amsn2.gui import base
import curses
from threading import Thread
from threading import Condition
import time
import sys

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._stdscr = parent._stdscr
        parent.setFocusedWindow(self)
        (y,x) = self._stdscr.getmaxyx()
        # TODO: Use a pad instead
        self._win = curses.newwin(y, int(0.25*x), 0, 0)
        self._win.bkgd(curses.color_pair(0))
        self._win.border()
        self._clwidget = aMSNContactListWidget(amsn_core, self)

    def show(self):
        self._win.refresh()

    def hide(self):
        self._stdscr.clear()
        self._stdscr.refresh()

    def _on_char_cb(self, ch):
        print >> sys.stderr, "Length is %d" % len(ch)
        print >> sys.stderr, "Received %s in Contact List" % ch.encode("UTF-8")
        if ch == "KEY_UP":
            self._clwidget.move(-1)
        elif ch == "KEY_DOWN":
            self._clwidget.move(1)
        elif ch == "KEY_NPAGE":
            self._clwidget.move(10)
        elif ch == "KEY_PPAGE":
            self._clwidget.move(-10)

class aMSNContactListWidget(base.aMSNContactListWidget):

    def __init__(self, amsn_core, parent):
        super(aMSNContactListWidget, self).__init__(amsn_core, parent)
        self._groups_order = []
        self._groups = {}
        self._contacts = {}
        self._win = parent._win
        self._stdscr = parent._stdscr
        self._mod_lock = Condition()
        self._modified = False
        self._thread = Thread(target=self.__thread_run)
        self._thread.daemon = True
        self._thread.setDaemon(True)
        self._thread.start()
        self._selected = 1

    def move(self, num):
        self._selected += num
        if self._selected < 1:
            self._selected = 1
        self.__repaint()


    def contactListUpdated(self, clView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            # TODO: Implement it to sort groups
            for g in self._groups_order:
                if g not in clView.group_ids:
                    self._groups.delete(g)
            for g in clView.group_ids:
                if not g in self._groups_order:
                    self._groups[g] = None
            self._groups_order = clView.group_ids
            self._modified = True

            # Notify waiting threads that we modified something
            self._mod_lock.notify()

    def groupUpdated(self, gView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            if self._groups.has_key(gView.uid):
                if self._groups[gView.uid] is not None:
                    #Delete contacts
                    for c in self._groups[gView.uid].contact_ids:
                        if c not in gView.contact_ids:
                            if self._contacts[c]['refs'] == 1:
                                self._contacts.delete(c)
                            else:
                                self._contacts[c]['refs'] -= 1
                #Add contacts
                for c in gView.contact_ids:
                    if not self._contacts.has_key(c):
                        self._contacts[c] = {'cView': None, 'refs': 1}
                        continue
                    #If contact wasn't already there, increment reference count
                    if self._groups[gView.uid] is None or c not in self._groups[gView.uid].contact_ids:
                        self._contacts[c]['refs'] += 1
                self._groups[gView.uid] = gView
                self._modified = True

                # Notify waiting threads that we modified something
                self._mod_lock.notify()

    def contactUpdated(self, cView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            if self._contacts.has_key(cView.uid):
                self._contacts[cView.uid]['cView'] = cView
                self._modified = True

                # Notify waiting threads that we modified something
                self._mod_lock.notify()

    def __repaint(self):
        # Acquire the lock to do modifications
        with self._mod_lock:
            self._win.clear()
            (y, x) = self._stdscr.getmaxyx()
            self._win.move(0,1)
            # How many screenfulls should we skip?
            skip = int((self._selected - 1) / (y - 2)) * (y - 2)
            available = y - 2
            list = []
            for g in self._groups_order:
                if self._groups[g] in None:
                    continue
                # If there is no display space available, exit the loop
                if available <= 0:
                    break
                # Check if we should skip some more lines
                if skip <= 0:
                    # If not, display the group
                    available -= 1
                    dis_groups += 1
                else:
                    # Otherwise skip the group name display, go on with checks for group contacts
                    skip -= 1
                gso.append(g)
                # If we must skip some more lines
                if skip > 0:
                    if skip >= len(self._groups[g].contact_ids):
                        # If we should skip the whole group, remove it from list and go on with next group
                        skip -= len(self._groups[g].contact_ids)
                        gso.pop()
                        continue
                # Otherwise just trim the contacts we should skip, limited to available display space
                gso[-1].contact_ids = gso[-1].contact_ids[skip:skip + available]
                skip = 0

                # Subtract from available display space the number of contacts currently on display
                available -= len(gso[-1].contact_ids)
            gso.reverse()
            skip = int((self._selected - 1) / (y - 2)) * (y - 2)
            i = 0
            for g in gso:
                if self._groups[g] is not None:
                    cids = self._groups[g].contact_ids
                    cids.reverse()
                    # Display contacts
                    for c in cids:
                        if self._contacts.has_key(c) and self._contacts[c]['cView'] is not None:
                            if i == y - 2 - (self._selected - skip):
                                self._win.bkgdset(curses.color_pair(1))
                            self._win.insstr(self._contacts[c]['cView'].name.toString())
                            self._win.bkgdset(curses.color_pair(0))
                            self._win.insch(' ')
                            self._win.insch(curses.ACS_HLINE)
                            self._win.insch(curses.ACS_HLINE)
                            self._win.insch(curses.ACS_LLCORNER)
                            self._win.insertln()
                            self._win.bkgdset(curses.color_pair(0))
                            i += 1
                    # Display group
                    if dis_groups > 0:
                        dis_groups -= 1
                        if i == y - 2 - (self._selected - skip):
                            self._win.bkgdset(curses.color_pair(1))
                        self._win.insstr(self._groups[g].name.toString())
                        self._win.bkgdset(curses.color_pair(0))
                        self._win.insch(' ')
                        self._win.insch(curses.ACS_LLCORNER)
                        self._win.insertln()
                        i += 1
            self._win.border()
            self._win.refresh()
            self._modified = False


    def __thread_run(self):
        while True:
            # We don't want to repaint too often, once every half second is cool
            time.sleep(0.5)
            with self._mod_lock:
                while not self._modified:
                    self._mod_lock.wait(timeout=1)
                self.__repaint()
