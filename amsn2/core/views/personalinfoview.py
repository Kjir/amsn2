from stringview import *
from imageview import *

def rw_property(f):
    return property(**f())

class PersonalInfoView(object):
    def __init__(self, personalinfo_manager):
        self._personalinfo_manager = personalinfo_manager

        self._nickname = StringView()
        self._psm = StringView()
        self._current_media  = StringView()
        self._image = ImageView()
        self._presence = 'offline'

        # TODO: get more info, how to manage webcams and mail
        self._webcam = None
        self._mail_unread = None

    def changeDP(self):
        self._personalinfo_manager._on_DP_change_request()

    @rw_property
    def nick():
        def fget(self):
            return self._nickname
        def fset(self, nick):
            self._personalinfo_manager._on_nick_changed(nick)
        return locals()

    @rw_property
    def psm():
        def fget(self):
            return self._psm
        def fset(self, psm):
            self._personalinfo_manager._on_PSM_changed(psm)
        return locals()

    @rw_property
    def dp():
        def fget(self):
            return self._image
        def fset(self, dp_msnobj):
            self._personalinfo_manager._on_DP_changed(dp_msnobj)
        return locals()

    @rw_property
    def current_media():
        def fget(self):
            return self._current_media
        def fset(self, artist, song):
            self._personalinfo_manager._on_CM_changed((artist, song))
        return locals()

    @rw_property
    def presence():
        def fget(self):
            return self._presence
        def fset(self, presence):
            self._personalinfo_manager._on_presence_changed(presence)
        return locals()

