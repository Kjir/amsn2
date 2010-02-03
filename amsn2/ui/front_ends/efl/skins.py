import os.path
from amsn2.ui import base

class Skin(base.Skin):
    def __init__(self, core, path):
        self._path = path
        self._dict = {}
        #TODO : remove, it's just here for test purpose
        #TODO : explain a bit :D
        self.set_key("buddy_online", ("Filename", "amsn2/themes/default/images/online.png"))
        self.set_key("emblem_online", ("Filename", "amsn2/themes/default/images/contact_list/plain_emblem.png"))

        self.set_key("buddy_away", ("Filename", "amsn2/themes/default/images/away.png"))
        self.set_key("emblem_away", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.set_key("buddy_brb", ("Filename", "amsn2/themes/default/images/away.png"))
        self.set_key("emblem_brb", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.set_key("buddy_idle", ("Filename", "amsn2/themes/default/images/away.png"))
        self.set_key("emblem_idle", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.set_key("buddy_lunch", ("Filename", "amsn2/themes/default/images/away.png"))
        self.set_key("emblem_lunch", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))

        # Just to show you can use an image from the edj file
        self.set_key("buddy_busy", ("EET", ("amsn2/themes/default.edj", "images/0")))
        self.set_key("emblem_busy", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))
        self.set_key("buddy_phone", ("EET", ("amsn2/themes/default.edj", "images/0")))
        self.set_key("emblem_phone", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))

        self.set_key("buddy_offline", ("Filename", "amsn2/themes/default/images/offline.png"))
        self.set_key("emblem_offline", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))
        self.set_key("buddy_hidden", ("Filename", "amsn2/themes/default/images/offline.png"))
        self.set_key("emblem_hidden", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))

        self.set_key("default_dp", ("Filename", "amsn2/themes/default/images/contact_list/nopic.png"))



    def get_key(self, key, default=None):
        try:
            return self._dict[key]
        except KeyError:
            return default

    def set_key(self, key, value):
        self._dict[key] = value




class SkinManager(base.SkinManager):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def set_skin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def get_skins(self, path):
        pass
