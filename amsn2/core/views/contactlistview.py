from stringview import *
from imageview import *
from menuview import *

class ContactListView:
    def __init__(self):
        self.group_ids = []



class GroupView:
    def __init__(self, core, uid, name, contact_ids=[], active=0):
        self.uid = uid
        self.contact_ids = set(contact_ids)
        self.icon = ImageView() # TODO: expanded/collapsed icon
        self.name = StringView() # TODO: default color from skin/settings
        self.name.append_text(name) #TODO: parse for smileys
        active = 0 #TODO
        total = len(self.contact_ids)
        self.name.append_text("(" + str(active) + "/" + str(total) + ")")

        self.on_click = None #TODO: collapse, expand
        self.on_double_click = None
        self.on_right_click_popup_menu = GroupPopupMenu(core)
        self.tooltip = None
        self.context_menu = None


    #TODO: @roproperty: context_menu, tooltip



""" a view of a contact on the contact list """
class ContactView:
    def __init__(self, core, amsn_contact):
        """
        @type core: aMSNCore
        @type amsn_contact: aMSNContact
        """

        self.uid = amsn_contact.uid

        self.icon = amsn_contact.icon
        #TODO: apply emblem on dp
        self.dp = amsn_contact.dp.clone()
        self.dp.append_imageview(amsn_contact.emblem)
        self.name = StringView() # TODO : default colors
        self.name.open_tag("nickname")
        self.name.append_stringview(amsn_contact.nickname) # TODO parse
        self.name.close_tag("nickname")
        self.name.append_text(" ")
        self.name.open_tag("status")
        self.name.append_text("(")
        self.name.append_stringview(amsn_contact.status)
        self.name.append_text(")")
        self.name.close_tag("status")
        self.name.append_text(" ")
        self.name.open_tag("psm")
        self.name.set_italic()
        self.name.append_stringview(amsn_contact.personal_message)
        self.name.unset_italic()
        self.name.close_tag("psm")
        #TODO:
        def start_conversation_cb(c_uid):
            core._conversation_manager.new_conversation([c_uid])
        self.on_click = start_conversation_cb
        self.on_double_click = None
        self.on_right_click_popup_menu = ContactPopupMenu(core, amsn_contact)
        self.tooltip = None
        self.context_menu = None

    #TODO: @roproperty: context_menu, tooltip

class ContactPopupMenu(MenuView):
    def __init__(self, core, amsncontact):
        MenuView.__init__(self)
        remove = MenuItemView(MenuItemView.COMMAND,
                              label="Remove %s" % amsncontact.account,
                              command= lambda:
                              core._contactlist_manager.remove_contact_Uid(amsncontact.uid))
        self.add_item(remove)

class GroupPopupMenu(MenuView):
    def __init__(self, core):
        MenuView.__init__(self)

