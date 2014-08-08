django-xadmin-extras
=====================

Extra features for `django-xadmin <http://www.github.com/django-xadmin>`_

New features:
-------------

  * Form wizard class working like django form wizard.
  * Allow adding custom menu entries via AppConfig.
  * `django-hstore <https://github.com/djangonauts/django-hstore>`_ support when editing objects.
  * Views for external apps:
  
  	+ `django-celery <https://github.com/celery/django-celery>`_
  	+ `django-settings <https://github.com/jqb/django-settings>`_
  	+ `django-mail-factory <https://github.com/novapost/django-mail-factory>`_


Form wizard
------------

Integrate Django FormWizards with xadmin views:

Any view using a wizard should inherit from FormWizardAdminView

.. code:: python

	from xadmin_extras.wizard import FormWizardAdminView, SessionWizardViewMixin

	class NotificateView(SessionWizardViewMixin, FormWizardAdminView):
	    """A wizard view working together with xadmin, using
	    SessionWizard backend
	
	    """
	    form_list = [SelectFilterForm, NotificateForm]
	    form_template = 'admin/fbapps/notificate_form.html'
	    title = 'FB Push notifications'


Other wizard backends are available: SessionWizardViewMixin and CookieWizardViewMixin

For more info about Form wizard, see `django documentation <https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-wizard/>`_

To register a view to be available at admin, with name and protected, use `register_view()`:

.. code:: python

	import xadmin
	xadmin.site.register_view(
	    r'fbapps/notificate/$', NotificateView,
	    name='fbapps_notification_view')


Custom menu entries
--------------------

Using an `AppConfig-like class <https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig>`_  (available for Django 1.7), custom entries can be added for the menu of each App.

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

.. code:: python

    import xadmin.views as views
    import xadmin_extras as views_extra

    xadmin.site.register(views.CommAdminView, views_extra.AppConfigViewMixin)  


django-hstore support
----------------------

Add the widget ``XadminHStoreWidget`` to your form definition:

.. code:: python

	from django_hstore.forms import DictionaryField
	from xadmin_extras.django_hstore.widgets import XAdminHStoreWidget
	from django import forms
	
	
	class HStoreForm(forms.Form):
		data = DictionaryField(widget=XadminHStoreWidget())
	
	
External apps support
----------------------

Apps with custom views are defined at ``ext`` folder


**django-celery**

	.. code:: python
	
		import xadmin_extras.ext.celery as ext_celery
		
		xadmin.site.register(
			ext_celery.celery_models.PeriodicTask, ext_celery.PeriodicTaskAdmin)
		xadmin.site.register(
			ext_celery.celery_models.IntervalSchedule,
			ext_celery.IntervalScheduleAdmin)
		xadmin.site.register(
			ext_celery.celery_models.CrontabSchedule,
			ext_celery.CrontabScheduleAdmin)
		

**django-settings**

	.. code:: python
	
		import xadmin_extras.ext.settings as ext_settings
		
		xadmin.site.register(ext_settings.models.Setting, ext_settings.SettingsAdmin)


**django-mail-factory**

	(By default, the mails will be at URL: /admin/mails/)
	
	.. code:: python
	
		from xadmin.views import CommAdminView, filter_hook, FormAdminView

		import xadmin_extras.ext.mailfactory as ext_mailfactory
		
		xadmin.site.register_view(
    			r'^mails/$', ext_mailfactory.MailListView, name='mail_factory_list')
		xadmin.site.register_view(
    			r'^mails/(?P<mail_name>.*)/$',ext_mailfactory.MailFormView, name='mail_factory_form')
		xadmin.site.register_view(
    			r'^mails/(?P<mail_name>.*)/preview/(?P<lang>\w+)/$',
    			ext_mailfactory.MailPreviewMessageView, name='mail_factory_preview_message')
		



