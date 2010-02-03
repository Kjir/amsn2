import os
import Image
import logging
import papyon
import __builtin__
from views import AccountView
from views import StringView

logger = logging.getLogger('amsn2.core.account_manager')

class aMSNAccount(object):
    """ aMSNAccount : a Class to represent an aMSN account
    This class will contain all settings relative to an account
    and will store the protocol and GUI objects
    """
    #TODO: use the personnal info stuff instead of the view
    def __init__(self, core, accountview):
        """
        @type core: aMSNCore
        @type accountview: AccountView
        @type account_dir: str
        """

        self.view = accountview
        self.personalinfoview = core._personalinfo_manager._personalinfoview
        self.do_save = accountview.save
        self.backend_manager = core._backend_manager
        self.client = None
        self.lock()
        self.load()

    def sign_out(self):
        if self.do_save:
            self.save()
        self.backend_manager.clean()
        self.unlock()

    def lock(self):
        #TODO
        pass

    def unlock(self):
        #TODO
        pass

    def load(self):
        #TODO:
        self.config = self.backend_manager.load_config(self)

    def save(self):
        self.view.nick = self.personalinfoview.nick
        self.view.psm = self.personalinfoview.psm
        self.view.dp = self.personalinfoview.dp
        self.backend_manager.save_account(self)

    def set_dp(self, path):
        if path:
            try:
                im = Image.open(path)
                im.resize((96, 96), Image.BILINEAR)

                # Write the file and rename it instead of creating a tmpfile
                profile = self.client.profile
                dp_path_tmp = self.backend_manager.get_file_location_DP(self.view.email, profile.id, 'tmp')
                im.save(dp_path_tmp, "PNG")
                f = open(dp_path_tmp)
                dp_object = papyon.p2p.MSNObject(self.client.profile,
                                                 os.path.getsize(dp_path_tmp),
                                                 papyon.p2p.MSNObjectType.DISPLAY_PICTURE,
                                                 os.path.basename(path),
                                                 os.path.basename(path),
                                                 data=f)
                f.close()

                dp_path = self.backend_manager.get_file_location_DP(self.view.email, profile.id, dp_object._data_sha)
                os.rename(dp_path_tmp, dp_path)

            except OSError, e:
                # FIXME: on Windows, it's raised if dp_path already exists
                # http://docs.python.org/library/os.html#os.rename
                logger.error('Trying to overwrite a saved dp')
                return

            except IOError, e:
                logger.error(e)
                return

            else:
                self.client.msn_object_store.publish(dp_object)
                self.personalinfoview.dp = dp_object

class aMSNAccountManager(object):
    """ aMSNAccountManager : The account manager that takes care of storing
    and retreiving all the account.
    """
    def __init__(self, core, options):
        self._core = core
        self.reload()

        if options.account is not None:
            pv = [p for p in self.accountviews if p.email == options.account]
            if pv:
                pv = pv[0]
                self.accountviews.remove(pv)
            else:
                pv = AccountView(core, options.account)
                pv.password = options.password
            self.accountviews.insert(0, pv)

    def reload(self):
        self.accountviews = self._core._backend_manager.load_accounts()

    def get_all_accountviews(self):
        self.reload()
        return self.accountviews

    def get_available_accountviews(self):
        return [v for v in self.get_all_accountviews() if not self.is_account_locked(v)]

    def signin_to_account(self, accountview):
        """
        @type accountview: AccountView
        @rtype: aMSNAccount
        """

        acc = aMSNAccount(self._core, accountview)

        if accountview.save:
            self._core._backend_manager.switch_to_backend(accountview.preferred_backend)
            acc.backend_manager.save_account(acc)
        else:
            self._core._backend_manager.remove_account(accountview.email)
            self._core._backend_manager.switch_to_backend('nullbackend')
        acc.backend_manager.set_account(accountview.email)

        acc.lock()
        return acc

    def is_account_locked(self, accountview):
        """
        @type accountview: AccountView
        @rtype: bool
        @return: True if accountview is locked
        """

        #TODO
        return False

