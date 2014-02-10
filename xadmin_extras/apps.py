# coding=utf-8


class AdminAppMixin(object):

    def __init__(self):
        self.custom_menu = self.init_menu()

    def init_menu(self):
        """Add custom menu entries to the menu displayed for this app

        Return a list of dicts, each dict will be a entry for the submenu of
        the app:
            {'url': '/admin/.../', 'icon': 'bolt', 'title': 'Custom'}
        also 'perm' and 'order' keys can be added.

        """
        return {}
