import os.path
from amsn2.ui import base

class Skin(base.Skin):
    def __init__(self, core, path):
        self._path = path
        pass

    def get_key(self, key, default):
        pass

    def set_key(self, key, value):
        pass



class SkinManager(base.SkinManager):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def set_skin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def get_skins(self, path):
        pass
