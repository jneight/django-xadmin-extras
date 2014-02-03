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




