# coding=utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

import xadmin
import adminx

# based on xadmin's TestCase
class AppConfigTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.test_view_class = xadmin.site.get_view_class(
            xadmin.views.CommAdminView)
        self.test_view = self.test_view_class(
            self._mocked_request('test/comm'))

    def test_get_menu(self):
        generated_menu = self.test_view.get_apps_menu()
        self.assertEqual(generated_menu,
            {'app:testapp':
                {'title': 'Test App', 'url': '', 'perm': None,
                 'menus': [
                     {'url': '/admin/testapp/testurl/', 'title': u'Test URL',
                      'order': '', 'perm': None, 'icon': 'bolt'}],
                 'first_icon': 'test', 'order': ''}})

        final_menu = self.test_view.get_nav_menu()
        self.assertEqual(
            final_menu,
            [{'first_url': '/tests/modela/', 'title': 'Test App',
              'url': '', 'perm': None, 'menus': [
                  {'url': '/tests/modela/', 'icon': None, 'order': 1,
                   'perm': 'tests.view_modela', 'title': u'Model as'},
                  {'url': '/admin/testapp/testurl/', 'title': u'Test URL',
                   'order': '', 'perm': None, 'icon': 'bolt'}],
              'first_icon': 'test', 'order': ''},
             {'menus': [{'url': '/tests/modelb/', 'icon': None, 'order': 2,
                         'perm': 'tests.view_modelb', 'title': u'Model bs'}],
              'first_url': '/tests/modelb/', 'title': u'Tests'}])

    def _create_superuser(self, username):
        return User.objects.create(username=username, is_superuser=True)

    def _mocked_request(self, url, user='admin'):
        request = self.factory.get(url)
        request.user = isinstance(user, User) and user or self._create_superuser(user)
        request.session = {}
        return request
