# coding=utf-8

import copy

class AdminAppMixin(object):

    def init_menu(self):
        """Add custom menu entries to the menu displayed for this app

        Return a list of dicts, each dict will be a entry for the submenu of
        the app:
            {'url': '/admin/.../', 'icon': 'bolt', 'title': 'Custom'}
        also 'perm' and 'order' keys can be added.

        """
        return []

    def has_menu_permission(self, obj=None):
        return True
