from contactlist_manager import *
from conversation import aMSNConversation

class aMSNConversationManager:
    def __init__(self, core):
        """
        @type core: aMSNCore
        """

        self._core = core
        self._convs = []
        self._wins = []

    def on_invite_conversation(self, conversation):
        print "new conv"
        contacts_uid = [c.id for c in conversation.participants]
        #TODO: What if the contact_manager has not build a view for that contact?
        c = aMSNConversation(self._core, self, conversation, contacts_uid)
        self._convs.append(c)

    def new_conversation(self, contacts_uid):
        """ contacts_uid is a list of contact uid """
        #TODO: check if no conversation like this one already exists
        c = aMSNConversation(self._core, self, None, contacts_uid)
        self._convs.append(c)



    def get_conversation_window(self, amsn_conversation):
        #TODO:
        #contacts should be a list of contact view
        # for the moment, always create a new win
        win = self._core._ui_manager.load_chat_window(self)
        self._wins.append(win)
        return win


