
class basebackend():
    """
    Base backend, used as a model to implement others backends.
    It contains the functions that should be available for every backend.
    """

    def save_config(self, amsn_account, config):
        raise NotImplementedError

    def load_config(self, amsn_account):
        raise NotImplementedError

    def load_account(self, email):
        raise NotImplementedError

    def load_accounts(self):
        raise NotImplementedError

    def save_account(self, amsn_account):
        raise NotImplementedError

    def set_account(self, email):
        raise NotImplementedError

    def clean(self):
        """
        Delete temporary things and prepare the backend to be detached
        or to begin another session with the same backend (e.g. with nullbackend)
        """
        raise NotImplementedError


    """ DPs """
    def get_file_location_DP(self, email, uid, shaci):
        raise NotImplementedError

    def get_DPs(self, email):
        raise NotImplementedError
