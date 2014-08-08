# coding=utf-8

""":synopsis: Admin class to add django-settings to xadmin dashboard"""


from django.utils.translation import ugettext as _

from django_settings import dataapi, forms, models


class SettingsAdmin(object):
    """Just add support for django-settings to xadmin

    """
    model = models.Setting
    list_display = ['id', 'name', 'setting_type', '_get_setting_value']
    form = forms.SettingForm
    model_icon = 'edit'

    def _get_setting_value(self, obj):
        return dataapi.data.get(obj.name)
    _get_setting_value.short_description = _('Value')

    def _get_setting_model(self, instance, **kwargs):
        """When Using an instance, we can get the type of the data stored

        """
        return instance.setting_object.__class__

    def prepare_form(self):
        super(SettingsAdmin, self).prepare_form()
        self.model_form.setting_model = self._get_setting_model(
            **self.get_form_datas())

