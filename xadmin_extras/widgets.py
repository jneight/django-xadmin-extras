# coding=utf-8

from django import forms
from django.utils.safestring import mark_safe
from xadmin import widgets


class AdminDateButtonLessWidget(widgets.AdminDateWidget):
    def render(self, name, value, attrs=None):
        input_html = super(forms.DateInput, self).render(name, value, attrs)
        return mark_safe("""
            <div class="input-group date bootstrap-datepicker">
            <span class="input-group-addon">
            <i class="fa fa-calendar"></i>
            </span>{0}</div>""".format(input_html))


class AdminTimeStepsWidget(widgets.AdminTimeWidget):
    def render(self, name, value, attrs=None):
        input_html = super(forms.TimeInput, self).render(name, value, attrs)
        return mark_safe("""
            <div class="input-group time bootstrap-timepicker">
            <span class="input-group-addon">
            <i class="fa fa-clock-o"></i>
            </span>{0}</div>""".format(input_html))
