"""TODO:
    * Let the aMSNContactListWidget be selectable to choose contacts to add to a
    conversation... each contact should have a checkbox on front of it
    * Drag contacts through groups
    * Drag groups
    ...
"""


class aMSNContactListWindow(object):
    """ This interface represents the main Contact List Window
        self._clwiget is an aMSNContactListWidget 
    """
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here """
        raise NotImplementedError

    def show(self):
        """ Show the contact list window """
        raise NotImplementedError

    def hide(self):
        """ Hide the contact list window """
        raise NotImplementedError

    def set_title(self, text):
        """ This will allow the core to change the current window's title
        @type text: str
        """
        raise NotImplementedError

    def set_menu(self, menu):
        """ This will allow the core to change the current window's main menu
        @type menu: MenuView
        """
        raise NotImplementedError

    def my_info_updated(self, view):
        """ This will allow the core to change pieces of information about
        ourself, such as DP, nick, psm, the current media being played,...
        @type view: PersonalInfoView
        @param view: the PersonalInfoView of the ourself (contains DP, nick, psm,
        currentMedia,...)"""
        raise NotImplementedError

    def get_contactlist_widget(self):
        """This will allow the core to access the widget"""
        raise NotImplementedError

class aMSNContactListWidget(object):
    """ This interface implements the contact list of the UI """
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here """
        raise NotImplementedError

    def show(self):
        """ Show the contact list widget """
        raise NotImplementedError

    def hide(self):
        """ Hide the contact list widget """
        raise NotImplementedError

    def contactlist_updated(self, clView):
        """ This method will be called when the core wants to notify
        the contact list of the groups that it contains, and where they
        should be drawn a group should be drawn.
        It will be called initially to feed the contact list with the groups
        that the CL should contain.
        It will also be called to remove any group that needs to be removed.

        @type clView: ContactListView
        @param clView : contains the list of groups contained in
        the contact list which will contain the list of ContactViews
        for all the contacts to show in the group."""
        raise NotImplementedError

    def group_updated(self, groupView):
        """ This method will be called to notify the contact list
        that a group has been updated.
        The contact list should update its icon and name
        but also its content (the ContactViews). The order of the contacts
        may be changed, in which case the UI should update itself accordingly.
        A contact can also be added or removed from a group using this method
        """
        raise NotImplementedError

    def contact_updated(self, contactView):
        """ This method will be called to notify the contact list
        that a contact has been updated.
        The contact can be in any group drawn and his icon,
        name or DP should be updated accordingly.
        The position of the contact will not be changed by a call
        to this function. If the position was changed, a groupUpdated
        call will be made with the new order of the contacts
        in the affects groups.
        """
        raise NotImplementedError

