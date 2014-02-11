# coding=utf-8


from xadmin_extras.apps import AdminAppMixin


class TestAppConfig(AdminAppMixin):
    name = 'testapp'
    verbose_name = 'Test App'
    icon = 'test'

    def init_menu(self):
        return [{
            'url': '/admin/testapp/testurl/', 'icon': 'bolt',
            'title': u'Test URL', 'order': '', 'perm': None}]

