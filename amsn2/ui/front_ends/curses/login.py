import curses
import curses.textpad
import urwid
import logging
from amsn2.core.views import AccountView

logger = logging.getLogger('amsn2.curses.login')

class TextBox(object):
    def __init__(self, win, y, x, txt):
        self._win = win.derwin(1, 30, y, x)
        self._win.bkgd(' ', curses.color_pair(0))
        self._win.clear()
        self._txtbox = curses.textpad.Textbox(self._win)
        self._txtbox.stripspaces = True

        if txt is not None:
            self._insert(txt)

    def edit(self):
        return self._txtbox.edit()

    def value(self):
        return self._txtbox.gather()

    def _insert(self, txt):
        for ch in txt:
            self._txtbox.do_command(ch)

class PasswordBox(TextBox):
    def __init__(self, win, y, x, txt):
        self._password = ''
        super(PasswordBox, self).__init__(win, y, x, txt)

    def edit(self, cb=None):
        return self._txtbox.edit(self._validateInput)

    def value(self):
        return self._password

    def _validateInput(self, ch):
        if ch in (curses.KEY_BACKSPACE, curses.ascii.BS):
            self._password = self._password[0:-1]
            return ch
        elif curses.ascii.isprint(ch):
            self._password += chr(ch)
            return '*'
        else:
            return ch

    def _insert(self, str):
        for ch in str:
            self._password += ch
            self._txtbox.do_command('*')

class aMSNLoginWindow(object):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self.switch_to_profile(None)
        self._main = parent._main

    def show(self):
        self._username_t = urwid.Edit(("label", "Username:"))
        self._password_t = urwid.Edit(("label", "Password:"))
        self._main.widget.set_body(urwid.ListBox([self._username_t, self._password_t]))
        self._main.unhandled_input = self.handle_input
        self._main.draw_screen()

    def hide(self):
        self._username_t = None
        self._password_t = None

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.email
            self._password = self.current_profile.password

    def create_profile(self):
        self.current_profile.email = self._username_t.get_edit_text()
        self.current_profile.password = self._password_t.get_edit_text()
        return self.current_profile

    def on_connecting(self, progress, message):
        self._main.widget.body.get_body().set_text(message)

    def set_accounts(self, account_views):
        self.accounts = account_views
        #TODO: add autologin stuff, account selection
        if len(self.accounts) == 0:
            a = AccountView(self._amsn_core, "")
            self.switch_to_profile(a)
        for a in self.accounts:
            self.switch_to_profile(a)
            break

    def signin(self):
        self._username_t = None
        self._password_t = None
        self._main.widget.set_body(urwid.Filler(urwid.Text("Logging in..."), valign='middle'))

    def signout(self):
        pass

    def handle_input(self, k):
        if k == 'enter':
            self._amsn_core.signin_to_account(self, self.create_profile())
        else:
            print k
