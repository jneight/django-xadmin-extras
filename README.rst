django-xadmin-extras
=====================

Extra functionality for `django-xadmin <http://www.github.com/django-xadmin>`_


Form wizard
------------

Django FormWizards backend are working with xadmin views:

Any wizard view should inherit from FormWizardAdminView

.. code:: python

	from xadmin_extras.wizard import FormWizardAdminView, SessionWizardViewMixin

	class NotificateView(SessionWizardViewMixin, FormWizardAdminView):
	    """A wizard view working together with xadmin, using
	    SessionWizard backend
	
	    """
	    form_list = [SelectFilterForm, NotificateForm]
	    form_template = 'admin/fbapps/notificate_form.html'
	    title = 'FB Push notifications'


Any Wizard backend can be used, for now, SessionWizardViewMixin and CookieWizardViewMixin are provided.

For more info about Form wizard, see `django documentation <https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-wizard/>`_

To register view to be available at admin, use `register_view()`:

.. code:: python

	import xadmin
	xadmin.site.register_view(
	    r'fbapps/notificate/$', NotificateView,
	    name='fbapps_notification_view')


Custom menu entries
--------------------

Using an AppConfig-like class (available for Django 1.7), custom entries can be added for the menu of each App.

Create a file called `apps.py` at your app folder, create a class and edit `init_menu()`

.. code:: python

    # coding=utf-8

    # from django.apps import AppConfig (commented for django 1.6)
    from xadmin_extras.apps import AdminAppMixin


    class FooConfig(AdminAppMixin):
        """name and verbose_name are going to be used for django AppConfig too
        
        """
        name = 'foo'
        verbose_name = 'Foo app.'
        icon = 'foo'

        def init_menu(self):
            """Add custom menu entries to the menu displayed for this app

            Return a list of dicts, each dict will be a entry for the submenu of
            the app:
                {'url': '/admin/.../', 'icon': 'bolt', 'title': 'Custom'}
            also 'perm' and 'order' keys can be added.

            """
            return [{
                'url': '/admin/foo/notification/', 'icon': 'bolt',
                'title': u'Send notifications', 'order': '', 'perm': None}]


    APP_CONFIG = FooConfig()

Now, assign the app to each model you want to get grouped and register them

.. code:: python

    import xadmin
    import .models as models

    class AppAdmin(object):
        app_config = AppConfig
       
    xadmin.site.register(models.Foo, AppAdmin)


After that, you just need to extend CommAdminView (maybe you have already done this
if you wanted to change menu style, site title, base template, etc.), with
AppConfigViewMixin available at xadmin_extras.views


