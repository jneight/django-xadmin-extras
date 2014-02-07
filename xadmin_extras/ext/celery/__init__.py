# coding=utf-8

""":synopsis: Admin classes to add django-celery models to xadmin dashboard"""


import djcelery.models as celery_models
import djcelery.admin as celery_admin


class PeriodicTaskAdmin(object):
    """Support periodictasks from celery in xadmin

    """
    model = celery_models.PeriodicTask
    list_display = ['__unicode__', 'enabled']
    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab'),
            'classes': ('extrapretty', 'wide', ),
        }),
        ('Arguments', {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide', 'collapse'),
        }),
        ('Execution Options', {
            'fields': ('expires', 'queue', 'exchange', 'routing_key'),
            'classes': ('extrapretty', 'wide', 'collapse'),
        }),)
    form = celery_admin.periodic_task_form()
    model_icon = 'calendar'


class IntervalScheduleAdmin(object):
    """Interval model"""

    model = celery_models.IntervalSchedule
    model_icon = 'calendar'


class CrontabScheduleAdmin(object):
    """Crontab model"""

    model = celery_models.CrontabSchedule
    model_icon = 'calendar'

