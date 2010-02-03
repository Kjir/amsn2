
class aMSNBackendManager(object):
    def __init__(self, core):
        self._backend = None
        self._core = core
        self.switch_to_backend('nullbackend')

    def set_backend_for_func(self, funcname, backend):
        try:
            f = getattr(backend, funcname)
            self.__setattr__(funcname, f)
        except AttributeError:
            self.__setattr__(funcname, self.__missing_func)

    def switch_to_backend(self, backend):
        try:
            m = __import__(backend, globals(), locals(), [], -1)
        except ImportError:
            m = __import__('defaultbackend', globals(), locals(), [], -1)
            print 'Trying to switch to non existent backend %s, using default instead' % backend
        backend_class = getattr(m, backend)

        del self._backend
        self._backend = backend_class()
        self._backend._core = self._core
        self.current_backend = backend

        # Config management methods
        self.set_backend_for_func('save_config', self._backend)
        self.set_backend_for_func('load_config', self._backend)

        # Account management methods
        self.set_backend_for_func('load_account', self._backend)
        self.set_backend_for_func('load_accounts', self._backend)
        self.set_backend_for_func('save_account', self._backend)
        self.set_backend_for_func('set_account', self._backend)
        self.set_backend_for_func('remove_account', self._backend)
        self.set_backend_for_func('clean', self._backend)

        # DP
        self.set_backend_for_func('get_file_location_DP', self._backend)

        # Logs management methods
        # MSNObjects cache methods (Smileys, DPs, ...)
        # Webcam sessions methods
        # Files received
        # ...

    def __missing_func(*args):
        print 'Function missing for %s' % self.current_backend


