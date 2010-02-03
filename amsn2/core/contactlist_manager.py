from views import *
import os
import tempfile
import papyon


class aMSNContactListManager:
    def __init__(self, core):
        """
        @type core: aMSNCore
        """

        self._core = core
        self._em = core._event_manager
        self._contacts = {} #Dictionary where every contact_uid has an associated aMSNContact
        self._groups = {}
        self._papyon_addressbook = None

    #TODO: sorting contacts & groups

    ''' normal changes of a contact '''

    def on_contact_changed(self, papyon_contact):
        """ Called when a contact changes either its presence, nick, psm or current media."""

        #1st/ update the aMSNContact object
        c = self.get_contact(papyon_contact.id, papyon_contact)
        c.fill(papyon_contact)
        #2nd/ update the ContactView
        cv = ContactView(self._core, c)
        self._em.emit(self._em.events.CONTACTVIEW_UPDATED, cv)

        #TODO: update the group view

    def on_contact_DP_changed(self, papyon_contact):
        """ Called when a contact changes its Display Picture. """

        #Request the DP...
        c = self.get_contact(papyon_contact.id, papyon_contact)
        if ("Theme", "dp_nopic") in c.dp.imgs:
            c.dp.load("Theme", "dp_loading")
        elif papyon_contact.msn_object is None:
            c.dp.load("Theme", "dp_nopic")
            self._em.emit(self._em.events.AMSNCONTACT_UPDATED, c)
            cv = ContactView(self._core, c)
            self._em.emit(self._em.events.CONTACTVIEW_UPDATED, cv)
            return

        if (papyon_contact.presence is not papyon.Presence.OFFLINE and
            papyon_contact.msn_object):
            self._core._account.client.msn_object_store.request(papyon_contact.msn_object,
                                                                (self.on_DP_downloaded,
                                                                 papyon_contact.id))

    def on_DP_downloaded(self, msn_object, uid):
        #1st/ update the aMSNContact object
        try:
            c = self.get_contact(uid)
        except ValueError:
            return
        fn = self._core._backend_manager.get_file_location_DP(c.account, uid,
                                                           msn_object._data_sha)
        try:
            f = open(fn, 'w+b', 0700)
            try:
                f.write(msn_object._data.read())
            finally:
                f.close()
        except IOError:
            return
        c.dp.load("Filename", fn)
        self._em.emit(self._em.events.AMSNCONTACT_UPDATED, c)
        #2nd/ update the ContactView
        cv = ContactView(self._core, c)
        self._em.emit(self._em.events.CONTACTVIEW_UPDATED, cv)

    ''' changes to the address book '''

# actions from user: accept/decline contact invitation - block/unblock contact - add/remove/rename group - add/remove contact to/from group

    def add_contact(self):
        def cb(email, invite_msg):
            if email:
                self._papyon_addressbook.add_messenger_contact(email, self._core._account.view.email,
                                                               invite_msg)
        self._core._ui_manager.load_contact_input_window(cb)

    def on_contact_added(self, contact):
        c = self.get_contact(contact.id, contact)
        gids = [ g.id for g in self.get_groups(contact.id)]
        self._add_contact_to_groups(contact.id, gids)
        self._core._ui_manager.show_notification("Contact %s added!" % contact.account)

    def remove_contact(self):
        def contact_cb(account):
            if account:
                try:
                    papyon_contact = self._papyon_addressbook.\
                                          contacts.search_by('account', account)[0]
                except IndexError:
                    self._core._ui_manager.show_error('You don\'t have the %s contact!', account)
                    return

                self.remove_contact_Uid(papyon_contact.id)

        self._core._ui_manager.load_contact_delete_window(contact_cb)

    def remove_contact_Uid(self, uid):
        papyon_contact = self._papyon_addressbook.contacts.search_by('id', uid)[0]
        def cb_ok():
            self._papyon_addressbook.delete_contact(papyon_contact)

        self._core._ui_manager.show_dialog('Are you sure you want to remove the contact %s?'
                                          % papyon_contact.account,
                                          (('OK', cb_ok), ('Cancel', lambda : '')))

    def on_contact_removed(self, contact):
        self._remove_contact_from_groups(contact.id)
        del self._contacts[contact.id]
        self._core._ui_manager.show_notification("Contact %s removed!" % contact.account)

    ''' additional methods '''

    # used when a contact is deleted, moved or change status to offline
    def _remove_contact_from_groups(self, cid):
        groups = self.get_groups(cid)
        for g in groups:
            g.contacts.remove(cid)
            gv = GroupView(self._core, g.id, g.name, g.contacts)
            self._em.emit(self._em.events.GROUPVIEW_UPDATED, gv)

    def _add_contact_to_groups(self, cid, gids):
        for gid in gids:
            g = self.get_group(gid)
            g.contacts.add(cid)
            gv = GroupView(self._core, g.id, g.name, g.contacts)
            self._em.emit(self._em.events.GROUPVIEW_UPDATED, gv)

        c = self.get_contact(cid)
        cv = ContactView(self._core, c)
        self._em.emit(self._em.events.CONTACTVIEW_UPDATED, cv)

    def on_CL_downloaded(self, address_book):
        self._papyon_addressbook = address_book
        grpviews = []
        cviews = []
        clv = ContactListView()

        for group in address_book.groups:
            contacts = address_book.contacts.search_by_groups(group)

            for contact in contacts:
                c = self.get_contact(contact.id, contact)
                cv = ContactView(self._core, c)
                cviews.append(cv)

            cids = [c.id for c in contacts]
            gv = GroupView(self._core, group.id, group.name, cids)
            grpviews.append(gv)
            clv.group_ids.append(group.id)

            self.get_group(group.id, group)

        contacts = address_book.contacts.search_by_memberships(papyon.Membership.FORWARD)
        no_group_ids= []
        for contact in contacts:
            if len(contact.groups) == 0:
                c = self.get_contact(contact.id, contact)
                cv = ContactView(self._core, c)
                cviews.append(cv)
                no_group_ids.append(contact.id)

        if len(no_group_ids) > 0:
            gv = GroupView(self._core, 0, "NoGroup", no_group_ids)
            grpviews.append(gv)
            clv.group_ids.append(0)
            self.get_group(0, None, no_group_ids)

        #Emit the events
        self._em.emit(self._em.events.CLVIEW_UPDATED, clv)
        for g in grpviews:
            self._em.emit(self._em.events.GROUPVIEW_UPDATED, g)
        for c in cviews:
            self._em.emit(self._em.events.CONTACTVIEW_UPDATED, c)

    def get_contact(self, uid, papyon_contact=None):
        """
        @param uid: uid of the contact
        @type uid: str
        @param papyon_contact:
        @type papyon_contact:
        @return: aMSNContact of that contact
        @rtype: aMSNContact
        """
        #TODO: should raise UnknownContact or sthg like that
        try:
            return self._contacts[uid]
        except KeyError:
            if papyon_contact is not None:
                c = aMSNContact(self._core, papyon_contact)
                self._contacts[uid] = c
                self._em.emit(self._em.events.AMSNCONTACT_UPDATED, c)
                return c
            else:
                raise ValueError

    def get_group(self, gid, papyon_group = None, cids=[]):
        """
        @param gid: uid of the group
        @type gid: str
        @param papyon_group:
        @type papyon_group:
        @return: aMSNGroup of that group
        @rtype: aMSNGroup
        """
        try:
            return self._groups[gid]
        except KeyError:
            if papyon_group:
                contacts = self._papyon_addressbook.contacts.search_by_groups(papyon_group)
                g = aMSNGroup([c.id for c in contacts], papyon_group)
                self._groups[gid] = g
                # is AMSNGROUP_UPDATED necessary?
            elif gid == 0:
                g = aMSNGroup(cids)
                self._groups[0] = g
            else:
                raise ValueError

    def get_groups(self, uid):
        # propagate a ValueError
        return [self.get_group(gid) for gid in self.get_contact(uid).groups]


""" A few things used to describe a contact
    They are stored in that structure so that there's no need to create them
    everytime
"""
class aMSNContact():
    def __init__(self, core, papyon_contact=None):
        """
        @type core: aMSNCore
        @param papyon_contact:
        @type papyon_contact: papyon.profile.Contact
        """
        self._core = core

        self.account  = ''
        self.groups = set()
        self.dp = ImageView()
        self.icon = ImageView()
        self.emblem = ImageView()
        self.nickname = StringView()
        self.status = StringView()
        self.personal_message = StringView()
        self.current_media = StringView()
        if papyon_contact:
            if papyon_contact.msn_object is None:
                self.dp.load("Theme", "dp_nopic")
            else:
                self.dp.load("Theme", "dp_loading")
            self.fill(papyon_contact)

        else:
            self.dp.load("Theme", "dp_nopic")
            self.uid = None

    def fill(self, papyon_contact):
        """
        Fills the aMSNContact structure.

        @type papyon_contact: papyon.profile.Contact
        """

        self.uid = papyon_contact.id
        self.account = papyon_contact.account
        self.icon.load("Theme","buddy_" + self._core.p2s[papyon_contact.presence])
        self.emblem.load("Theme", "emblem_" + self._core.p2s[papyon_contact.presence])
        #TODO: PARSE ONLY ONCE
        self.nickname.reset()
        self.nickname.append_text(papyon_contact.display_name)
        self.personal_message.reset()
        self.personal_message.append_text(papyon_contact.personal_message)
        self.current_media.reset()
        self.current_media.append_text(papyon_contact.current_media)
        self.status.reset()
        self.status.append_text(self._core.p2s[papyon_contact.presence])

        #DP:
        if papyon_contact.msn_object:
            fn = self._core._backend_manager.get_file_location_DP(
                    papyon_contact.account,
                    papyon_contact.id,
                    papyon_contact.msn_object._data_sha)
            if os.path.exists(fn):
                self.dp.load("Filename", fn)
            else:
                #TODO: request?
                pass
        # ro, can be changed indirectly with addressbook's actions
        self.memberships = papyon_contact.memberships
        self.contact_type = papyon_contact.contact_type
        for g in papyon_contact.groups:
            self.groups.add(g.id)
        if len(self.groups) == 0:
            self.groups.add(0)
        # ro
        self.capabilities = papyon_contact.client_capabilities
        self.infos = papyon_contact.infos.copy()
        #for the moment, we store the papyon_contact object, but we shouldn't have to

        #TODO: getPapyonContact(self, core...) or _papyon_contact?
        self._papyon_contact = papyon_contact

class aMSNGroup():
    def __init__(self, cids, papyon_group=None):
        self.contacts = set(cids)
        if papyon_group:
            self.name = papyon_group.name
            self.id = papyon_group.id
        else:
            self.name = 'NoGroup'
            self.id = 0

