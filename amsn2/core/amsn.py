# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from amsn2 import protocol
from amsn2.backend import aMSNBackendManager
from views import *
from account_manager import *
from contactlist_manager import *
from conversation_manager import *
from oim_manager import *
from theme_manager import *
from personalinfo_manager import *
from event_manager import *
from userinterface_manager import *
import sys
import papyon
import logging

# Top-level loggers
papyon_logger = logging.getLogger("papyon")
logger = logging.getLogger("amsn2")

class aMSNCore(object):
    def __init__(self, options):
        """
        Create a new aMSN Core. It takes an options class as argument
        which has a variable for each option the core is supposed to received.
        This is easier done using optparse.
        The options supported are :
           options.account = the account's username to use
           options.password = the account's password to use
           options.front_end = the front end's name to use
           options.debug = whether or not to enable debug output
        """
        self.p2s = {papyon.Presence.ONLINE:"online",
                    papyon.Presence.BUSY:"busy",
                    papyon.Presence.IDLE:"idle",
                    papyon.Presence.AWAY:"away",
                    papyon.Presence.BE_RIGHT_BACK:"brb",
                    papyon.Presence.ON_THE_PHONE:"phone",
                    papyon.Presence.OUT_TO_LUNCH:"lunch",
                    papyon.Presence.INVISIBLE:"hidden",
                    papyon.Presence.OFFLINE:"offline"}
        self.Presence = papyon.Presence

        self._options = options
        self._ui_name = None
        self._loop = None
        self._main = None
        self._account = None

        self._event_manager = aMSNEventManager(self)
        self._backend_manager = aMSNBackendManager(self)
        self._account_manager = aMSNAccountManager(self, options)
        self._theme_manager = aMSNThemeManager(self)
        self._contactlist_manager = aMSNContactListManager(self)
        self._oim_manager = aMSNOIMManager(self)
        self._conversation_manager = aMSNConversationManager(self)
        self._personalinfo_manager = aMSNPersonalInfoManager(self)
        self._ui_manager = aMSNUserInterfaceManager(self)

        # TODO: redirect the logs somewhere, something like ctrl-s ctrl-d for amsn-0.9x
        logging.basicConfig(level=logging.WARNING)

        if self._options.debug_protocol:
            papyon_logger.setLevel(logging.DEBUG)
        else:
            papyon_logger.setLevel(logging.WARNING)

        if self._options.debug_amsn2:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

        self.load_UI(self._options.front_end)

    def run(self):
        self._main.show()
        self._loop.run()

    def load_UI(self, ui_name):
        """
        @type ui_name: str
        @param ui_name: The name of the User Interface
        """

        self._ui_name = ui_name
        self._ui_manager.load_UI(ui_name)
        self._loop = self._ui_manager.get_loop()

    def switch_to_UI(self, ui_name):
        """
        @type ui_name: str
        @param ui_name: The name of the User Interface
        """

        #TODO: unloadUI + stop loops??? + loadUI + run
        pass

    def main_window_shown(self):
        self._ui_manager.load_splash()

        accounts = self._account_manager.get_available_accountviews()
        self._ui_manager.load_login(accounts)

        menu = self.create_main_menuview()
        self._main.set_menu(menu)

    def get_main_window(self):
        return self._main

    def signin_to_account(self, login_window, accountview):
        """
        @type login_window: aMSNLoginWindow
        @type accountview: AccountView
        """

        print "Signing in to account %s" % (accountview.email)
        self._account = self._account_manager.signin_to_account(accountview)
        self._account.login = login_window
        self._account.login.signin()
        self._account.client = protocol.Client(self, self._account)
        self._account.client.connect(accountview.email, accountview.password)

    def sign_out_of_account(self):
        accounts = self._account_manager.get_available_accountviews()
        self._ui_manager.load_login(accounts)
        self._account.client.logout()

    def connection_state_changed(self, account, state):
        """
        @type account: aMSNAccount
        @type state: L{papyon.event.ClientState}
        @param state: New state of the Client.
        """

        status_str = \
        {
            papyon.event.ClientState.CONNECTING : 'Connecting to server...',
            papyon.event.ClientState.CONNECTED : 'Connected',
            papyon.event.ClientState.AUTHENTICATING : 'Authenticating...',
            papyon.event.ClientState.AUTHENTICATED : 'Password accepted',
            papyon.event.ClientState.SYNCHRONIZING : 'Please wait while your contact list\nis being downloaded...',
            papyon.event.ClientState.SYNCHRONIZED : 'Contact list downloaded successfully.\nHappy Chatting'
        }

        if state in status_str:
            account.login.on_connecting((state + 1)/ 7., status_str[state])

        elif state == papyon.event.ClientState.OPEN:
            self._ui_manager.load_contactlist()
            self._personalinfo_manager.set_account(account)
            self._contactlist_manager.on_CL_downloaded(account.client.address_book)

        elif state == papyon.event.ClientState.CLOSED:
            accounts = self._account_manager.get_available_accountviews()
            self._ui_manager.load_login(accounts)
            self._account.sign_out()
            self._account = None

    def idler_add(self, func):
        """
        @type func: function
        """

        self._loop.idler_add(func)

    def timer_add(self, delay, func):
        """
        @type delay: int
        @param delay: delay in seconds?
        @type func: function
        """

        self._loop.timer_add(delay, func)

    def quit(self):
        if self._account:
            self._account.sign_out()
        if self._loop:
            self._loop.quit()
        logging.shutdown()
        sys.exit(0)

    def create_main_menuview(self):
        menu = MenuView()
        quitMenuItem = MenuItemView(MenuItemView.COMMAND, label="Quit",
                                    command = self.quit)
        logOutMenuItem = MenuItemView(MenuItemView.COMMAND, label="Log out",
                                      command = self.sign_out_of_account)
        mainMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Main")
        mainMenu.add_item(logOutMenuItem)
        mainMenu.add_item(quitMenuItem)

        addContactItem = MenuItemView(MenuItemView.COMMAND, label="Add Contact",
                                      command=self._contactlist_manager.add_contact)
        removeContact = MenuItemView(MenuItemView.COMMAND, label='Remove contact',
                                     command=self._contactlist_manager.remove_contact)

        contactsMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Contacts")
        contactsMenu.add_item(addContactItem)
        contactsMenu.add_item(removeContact)

        menu.add_item(mainMenu)
        menu.add_item(contactsMenu)

        return menu

