# coding=utf-8

""":synopsis: Integration with django-xadmin

"""

from xadmin.views import CommAdminView, filter_hook, FormAdminView

from django.http import Http404, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.template.base import TemplateDoesNotExist
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied

from mail_factory import exceptions as mail_exceptions
from mail_factory import factory
from mail_factory.views import MailPreviewMixin
from .utils import registered_mails_names


class MailListView(CommAdminView):
    template_name = 'mailfactory_extras/list.html'

    def init_request(self, *args, **kwargs):
        if not self.has_view_permission():
            raise PermissionDenied
        return super(MailListView, self).init_request(*args, **kwargs)

    def get_context(self):
        """Add mails to the context

        """
        context = super(MailListView, self).get_context()
        mail_list = registered_mails_names()

        context['mail_map'] = mail_list
        return context

    def get(self, *args, **kwargs):
        context = self.get_context()
        return self.template_response(context)

    def template_response(self, context):
        return TemplateResponse(self.request, self.template_name,
            context, current_app=self.admin_site.name)

    def has_view_permission(self, obj=None):
        return self.user.is_superuser


class MailFormView(MailPreviewMixin, FormAdminView):
    form_template = 'mailfactory_extras/form.html'

    def init_request(self, *args, **kwargs):
        if not self.has_view_permission():
            raise PermissionDenied

        self.mail_name = kwargs['mail_name']
        self.prepare_form()
        try:
            self.mail_class = factory.get_mail_class(self.mail_name)
        except mail_exceptions.MailFactoryError:
            raise Http404

        self.raw = 'raw' in self.request.POST
        self.send = 'send' in self.request.POST
        self.email = self.request.POST.get('email')

    def get_form_datas(self):
        data = super(MailFormView, self).get_form_datas()
        data['mail_class'] = self.mail_class
        return data

    @filter_hook
    def prepare_form(self):
        self.view_form = factory.get_mail_form(self.mail_name)

    @filter_hook
    def instance_forms(self):
        self.form_obj = self.view_form(**self.get_form_datas())

    def setup_forms(self):
        super(MailFormView, self).setup_forms()
        self.form_obj.helper.form_tag = False

    def form_valid(self, form):
        if self.raw:
            return HttpResponse('<pre>%s</pre>' %
                factory.get_raw_content(
                    self.mail_name, [settings.DEFAULT_FROM_EMAIL],
                    form.cleaned_data).message())
        if self.send:
            factory.mail(self.mail_name, [self.email], form.cleaned_data)
            self.message_user(
                '%s mail sent to %s' % (self.mail_name, self.email))
            return redirect('mail_factory_list')

        data = None
        if form:
            data = form.get_context_data()
            if hasattr(form, 'cleaned_data'):
                data.update(form.cleaned_data)
        try:
            html = factory.get_html_for(self.mail_name, data, cid_to_data=True)
        except TemplateDoesNotExist:
            return redirect('admin:mail_factory_html_not_found',
                mail_name=self.mail_name)
        else:
            return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        if self.valid_forms():
            return self.form_valid(self.form_obj)
        return self.get_response()

    def get_context(self):
        context = super(MailFormView, self).get_context()
        context['mail_name'] = self.mail_name

        preview_messages = {}
        for lang_code, lang_name in settings.LANGUAGES:
            message = self.get_mail_preview(self.mail_name, lang_code)
            preview_messages[lang_code] = message
        context['preview_messages'] = preview_messages

        return context
    def has_view_permission(self, obj=None):
        return self.user.is_superuser

    def has_add_permission(self, obj=None):
        return self.user.is_superuser

    def has_change_permission(self, obj=None):
        return self.user.is_superuser

    def has_delete_permission(self, obj=None):
        return self.user.is_superuser


class MailPreviewMessageView(MailPreviewMixin, MailListView):
    template_name = 'mailfactory_extras/preview_message.html'

    def init_request(self, *args, **kwargs):
        if not self.has_view_permission():
            raise PermissionDenied

        self.mail_name = kwargs['mail_name']
        self.lang = kwargs['lang']
        try:
            self.mail_class = factory.get_mail_class(self.mail_name)
        except mail_exceptions.MailFactoryError:
            raise Http404

    def get_context(self):
        context = super(CommAdminView, self).get_context()
        context['message'] = self.get_mail_preview(self.mail_name, self.lang)
        context['mail_name'] = self.mail_name
        return context


#xadmin.site.register_view(
    #r'^mails/$', MailListView, name='mail_factory_list')
#xadmin.site.register_view(
    #r'^mails/(?P<mail_name>.*)/$',MailFormView, name='mail_factory_form')
#xadmin.site.register_view(
    #r'^mails/(?P<mail_name>.*)/preview/(?P<lang>\w+)/$',
    #MailPreviewMessageView, name='mail_factory_preview_message')
##xadmin.site.register_view(
    ##r'^mails/(?P<mail_name>.*)/html_not_found/$',
    ##MailHtmlNotFoundView, name='mail_factory_html_not_found')

