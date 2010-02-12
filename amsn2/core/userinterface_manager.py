# -*- coding: utf-8 -*-

from views import *

import logging
logger = logging.getLogger('amsn2.ui_manager')

class aMSNUserInterfaceManager(object):
    front_ends = {}
    def __init__(self, core):
        self._core = core
        self._ui = None
        self._splash = None
        self._login = None
        self._contactlist = None

    @staticmethod
    def register_frontend(name, module):
        aMSNUserInterfaceManager.front_ends[name] = module

    @staticmethod
    def list_frontends():
        return aMSNUserInterfaceManager.front_ends.keys()

    @staticmethod
    def frontend_exists(front_end):
        return front_end in aMSNUserInterfaceManager.list_frontends()

    def load_UI(self, ui_name):
        if self.frontend_exists(ui_name):
            self._ui = self.front_ends[ui_name].load()

            self._loop = self._ui.aMSNMainLoop(self)
            self._main = self._ui.aMSNMainWindow(self._core)
            self._core._main = self._main
            self._skin_manager = self._ui.SkinManager(self._core)
            self._core._skin_manager = self._skin_manager

        else:
            logger.error('Unable to load UI %s. Available front ends are: %s'
                         % (ui_name, str(self.list_frontends())))
            self._core.quit()

    def get_loop(self):
        return self._loop

    def load_splash(self):
        self._splash = self._ui.aMSNSplashScreen(self._core, self._main)
        image = ImageView()
        image.load("Filename","/path/to/image/here")

        self._splash.image = image
        self._splash.text = "Loading..."
        self._splash.show()
        self._main.title = "aMSN 2 - Loading"
        return self._splash

    def load_login(self, accounts):
        if self._splash:
            self._splash.hide()
            self._splash = None

        if self._contactlist:
            self.unload_contactlist()

        if not self._login:
            self._login = self._ui.aMSNLoginWindow(self._core, self._main)
            self._login.set_accounts(accounts)
            if accounts and accounts[0].autologin:
                self._core.signin_to_account(self._login, accounts[0])
        else:
            self._login.signout()
            self._login.set_accounts(accounts)

        self._main.title = "aMSN 2 - Login"

        self._login.show()

    def unload_login(self):
        self._login.hide()
        self._login = None

    def load_contactlist(self):
        self._contactlist = self._ui.aMSNContactListWindow(self._core, self._main)

        em = self._core._event_manager
        em.register(em.events.PERSONALINFO_UPDATED, self._contactlist.my_info_updated)

        clwidget = self._contactlist.get_contactlist_widget()
        em.register(em.events.CLVIEW_UPDATED, clwidget.contactlist_updated)
        em.register(em.events.GROUPVIEW_UPDATED, clwidget.group_updated)
        em.register(em.events.CONTACTVIEW_UPDATED, clwidget.contact_updated)

        if self._login:
            self.unload_login()

        self._main.title = "aMSN 2"
        self._contactlist.show()

    def unload_contactlist(self):
        self._contactlist.hide()

        em = self._core._event_manager
        em.unregister(em.events.PERSONALINFO_UPDATED, self._contactlist.my_info_updated)

        clwidget = self._contactlist.get_contactlist_widget()
        em.unregister(em.events.CLVIEW_UPDATED, clwidget.contactlist_updated)
        em.unregister(em.events.GROUPVIEW_UPDATED, clwidget.group_updated)
        em.unregister(em.events.CONTACTVIEW_UPDATED, clwidget.contact_updated)

        self._contactlist = None

    def show_dialog(self, message, buttons):
        self._ui.aMSNDialogWindow(message, buttons)

    def show_notification(self, message):
        self._ui.aMSNNotificationWindow(message)

    def show_error(self, message):
        self._ui.aMSNErrorWindow(message)

    def load_chat_window(self, conv_manager):
        return self._ui.aMSNChatWindow(conv_manager)

    def load_chat_widget(self, conversation, window, cuids):
        return self._ui.aMSNChatWidget(conversation, window, cuids)

    def load_contact_input_window(self, callback):
        return self._ui.aMSNContactInputWindow(('Contact to add: ', 'Invite message: '),
                                                 callback, ())

    def load_contact_delete_window(self, callback):
        return self._ui.aMSNContactDeleteWindow('Contact to remove: ', callback, ())

    def load_DP_chooser_window(self):
        self._ui.aMSNDPChooserWindow(self._core._account.set_dp ,self._core._backend_manager)

    # Common methods for all UI

    def get_accountview_from_email(self, email):
        """
        Search in the list of accounts and return the view of the given email

        @type email: str
        @param email: email to find
        @rtype: AccountView
        @return: Returns AccountView if it was found, otherwise return None
        """

        accv = [accv for accv in self._login._account_views if accv.email == email]

        if len(accv) == 0:
            return AccountView(self._core, email)
        else:
            return accv[0]



