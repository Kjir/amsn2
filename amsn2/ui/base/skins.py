import os.path

class Skin(object):
    def __init__(self, core, path):
        """
        @type core: aMSNCore
        @type path:
        """

        self._path = path
        pass

    def key_get(self, key, default):
        pass

    def key_set(self, key, value):
        pass



class SkinManager(object):
    def __init__(self, core):
        """
        @type core: aMSNCore
        """
        self._core = core
        self.skin = Skin(core, "skins")

    def skin_set(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))
        pass

    def get_skins(self, path):
        pass
