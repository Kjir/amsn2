from stringview import *

class MessageView:
    MESSAGE_INCOMING = 0
    MESSAGE_OUTGOING = 1
    def __init__(self):
        self.msg = StringView()
        self.sender = StringView()
        self.sender_icon = None
        self.message_type = MessageView.MESSAGE_INCOMING


    #TODO: toMessageStyle or sthg like that

    def to_stringview(self):
        strv = StringView()
        strv.append_stringview(self.sender)
        strv.append_text(" says:\n")
        strv.append_stringview(self.msg)
        strv.append_text("\n")

        return strv

