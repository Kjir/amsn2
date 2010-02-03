from constants import *
import evas
import ecore
import elementary
import skins
import window
from amsn2.ui import base
from amsn2.core.views import ContactView, StringView
from constants import *

class aMSNChatWindow(window.aMSNWindow, base.aMSNChatWindow):
    def __init__(self, conversation_manager):
        self._conversation_manager = conversation_manager
        window.aMSNWindow.__init__(self, conversation_manager._core)
        self._container = aMSNChatWidgetContainer()
        self.set_title(TITLE + " - Chatwindow")
        self.resize(CW_WIDTH, CW_HEIGHT)

        self.autodel_set(True)

    def add_chat_widget(self, chat_widget):
        self.resize_object_add(chat_widget)
        chat_widget.show()
        print chat_widget.ine.geometry
        print chat_widget.insc.geometry

#TODO: ChatWidgetContainer
class aMSNChatWidgetContainer:
    pass




class aMSNChatWidget(elementary.Box, base.aMSNChatWidget):
    def __init__(self, amsn_conversation, parent, contacts_uid):
        self._parent = parent
        elementary.Box.__init__(self, parent)
        self.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.homogenous_set(False)
        self._parent.resize_object_add(self)
        self.show()
        self._amsn_conversation = amsn_conversation

        self.outsc = elementary.Scroller(parent)
        self.outsc.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                        evas.EVAS_HINT_EXPAND)
        self.outsc.size_hint_align_set(evas.EVAS_HINT_FILL,
                                       evas.EVAS_HINT_FILL)
        self.outsc.policy_set(elementary.ELM_SCROLLER_POLICY_AUTO,
                              elementary.ELM_SCROLLER_POLICY_ON)
        self.outsc.bounce_set(False, True)
        self.pack_end(self.outsc)

        self.outbx = elementary.Box(parent)
        self.outbx.size_hint_weight_set(evas.EVAS_HINT_EXPAND, evas.EVAS_HINT_EXPAND)
        self.outbx.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.outsc.content_set(self.outbx)
        self.outbx.show()
        self.outsc.show()

        self.inbx = elementary.Box(parent)
        self.inbx.horizontal_set(True)
        self.inbx.homogenous_set(False)
        self.inbx.size_hint_weight_set(evas.EVAS_HINT_EXPAND, 0.0)
        self.inbx.size_hint_align_set(evas.EVAS_HINT_FILL, 0.5)
        self.pack_end(self.inbx)

        self.insc = elementary.Scroller(parent)
        self.insc.policy_set(elementary.ELM_SCROLLER_POLICY_AUTO,
                             elementary.ELM_SCROLLER_POLICY_AUTO)
        self.insc.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                       evas.EVAS_HINT_EXPAND)
        self.insc.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.inbx.pack_end(self.insc)

        self.ine = elementary.Entry(parent)
        self.ine.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                      evas.EVAS_HINT_EXPAND)
        self.ine.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        self.ine.event_callback_add(evas.EVAS_CALLBACK_KEY_DOWN, self.__ine_key_down);
        self.insc.content_set(self.ine)
        self.ine.show()
        self.insc.show()

        self.inb = elementary.Button(parent)
        self.inb.label_set("Send")
        self.inb.callback_clicked_add(self.__sendButton_cb, self.ine)
        self.inbx.pack_end(self.inb)
        self.inb.show()
        self.inbx.show()

        self.show()

    def __ine_key_down(self, obj, keydown):
        if (keydown.keyname == "Return"):
            ctrl = keydown.modifier_is_set("Control")
            alt = keydown.modifier_is_set("Alt")
            shift = keydown.modifier_is_set("Shift")
            win = keydown.modifier_is_set("Super") or keydown.modifier_is_set("Hyper")
            if (not ctrl and not alt and not shift and not win):
                #TODO: Remove \n
                str = obj.entry_get()
                obj.entry_set("")
                self.__send_msg(str)
        elif (keydown.keyname == "Up"):
            ctrl = keydown.modifier_is_set("Control")
            alt = keydown.modifier_is_set("Alt")
            shift = keydown.modifier_is_set("Shift")
            win = keydown.modifier_is_set("Super") or keydown.modifier_is_set("Hyper")
            if (ctrl and not alt and not shift and not win):
                print "TODO: UP => prev msg"
        elif (keydown.keyname == "Down"):
            ctrl = keydown.modifier_is_set("Control")
            alt = keydown.modifier_is_set("Alt")
            shift = keydown.modifier_is_set("Shift")
            win = keydown.modifier_is_set("Super") or keydown.modifier_is_set("Hyper")
            if (ctrl and not alt and not shift and not win):
                print "TODO: DOWN => prev msg"

    def __sendMsg(self, msg):
        bb = elementary.Bubble(self.parent)
        bb.label_set("TODO: MYSELF")
        bb.info_set("TODO: TIMESTAMP")
        #TODO: bb.icon_set()
        bb.size_hint_weight_set(evas.EVAS_HINT_EXPAND, 0.0)
        bb.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ab = elementary.AnchorBlock(self.parent)
        ab.text_set(msg)
        bb.content_set(ab)
        ab.show()
        self.outbx.pack_end(bb)
        bb.show()

        strv = StringView()
        strv.append_text(msg)
        self._amsn_conversation.send_message(strv)

    def __sendButton_cb(button, entry):
        str = entry.entry_get()
        entry.entry_set("")
        self.__sendMsg(msg)

    def on_user_joined(self, contact):
        print "%s joined the conversation" % (contact,)

    def on_user_left(self, contact):
        print "%s left the conversation" % (contact,)

    def on_user_typing(self, contact):
        print "%s is typing" % (contact,)

    def on_message_received(self, messageview, formatting=None):
        print "MSG RECEIVED"
        bb = elementary.Bubble(self.parent)
        bb.label_set("TODO: CONTACT")
        bb.info_set("TODO: TIMESTAMP")
        #TODO: bb.icon_set()
        bb.size_hint_weight_set(evas.EVAS_HINT_EXPAND, 0.0)
        bb.size_hint_align_set(evas.EVAS_HINT_FILL, evas.EVAS_HINT_FILL)
        ab = elementary.AnchorBlock(self.parent)
        ab.text_set(str(messageview.toStringView()))
        bb.content_set(ab)
        ab.show()
        self.outbx.pack_end(bb)
        bb.show()

    def nudge(self):
        #TODO
        print "Nudge received!!!"
