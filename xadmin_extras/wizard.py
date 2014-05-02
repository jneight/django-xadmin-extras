# coding=utf-8

from django.contrib.formtools.wizard.views import WizardView
from django.utils.decorators import classonlymethod
from django.template.response import TemplateResponse
from functools import update_wrapper

from xadmin.views.form import FormAdminView, csrf_protect_m, filter_hook


class FormWizardAdminView(WizardView, FormAdminView):
    form_list = None

    @classonlymethod
    def as_view(cls, *args, **kwargs):
        return cls.as_view()

    def __init__(self, request, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.__dict__.update(locals())
        super(FormAdminView, self).__init__(request, *args, **kwargs)

    @classonlymethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            initkwargs = cls.get_initkwargs(*args, **kwargs)
            self = cls(request, **initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            if self.request_method in self.http_method_names:
                handler = getattr(
                    self, self.request_method, self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            return handler(request, *args, **kwargs)
        update_wrapper(view, cls, updated=())
        view.need_site_permission = cls.need_site_permission
        return view

    def init_request(self, *args, **kwargs):
        self.dispatch(self.request, *args, **kwargs)

    def get_form(self, step=None, data=None, files=None):
        """Instanciate the form for the current step

        FormAdminView from xadmin expects form to be at self.form_obj

        """
        self.form_obj = super(FormWizardAdminView, self).get_form(
            step=step, data=data, files=files)
        return self.form_obj

    def prepare_form(self):
        """call `self.get_form()` to support form steps, etc."""
        raise NotImplementedError("Just use get_form() method instead")

    def instance_forms(self):
        """call `self.get_form()` to support form steps, etc."""
        raise NotImplementedError("Just use get_form() method instead")

    def post_response(self):
        raise NotImplementedError("Overwrite post() method")

    def get_response(self):
        raise NotImplementedError("Overwrite get() method")

    def render(self, form=None, **kwargs):
        """Returns the ``HttpResponse`` with the context data"""
        context = self.get_context(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context):
        """Add django-crispy form helper and draw the template

        Returns the ``TemplateResponse`` ready to be displayed

        """
        self.setup_forms()
        return TemplateResponse(
            self.request, self.form_template,
            context, current_app=self.admin_site.name)

    def get_context(self, **kwargs):
        """Use this method to built context data for the template

        Mix django wizard context data with django-xadmin context

        """
        context = self.get_context_data(form=self.form_obj, **kwargs)
        context.update(super(FormAdminView, self).get_context())
        return context

    @csrf_protect_m
    @filter_hook
    def get(self, request, *args, **kwargs):
        self.storage.reset()
        # reset the current step to the first step.
        self.storage.current_step = self.steps.first
        return self.render(self.get_form())

    @csrf_protect_m
    @filter_hook
    def post(self, request, *args, **kwargs):
        return super(FormWizardAdminView, self).post(request, *args, **kwargs)

    def done(self, *args, **kwargs):
        raise NotImplementedError("Your %s class has not defined a done() "
            "method, which is required." % self.__class__.__name__)


class SessionWizardViewMixin(object):
    """A WizardView with pre-configured SessionStorage backend.

    """
    storage_name = 'django.contrib.formtools.wizard.storage.session.SessionStorage'


class CookieWizardViewMixin(object):
    """A WizardView with pre-configured CookieStorage backend.

    """
    storage_name = 'django.contrib.formtools.wizard.storage.cookie.CookieStorage'
