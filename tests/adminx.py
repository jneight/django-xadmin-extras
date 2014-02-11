# coding=utf-8


import xadmin
import xadmin.views as views

import xadmin_extras.views as ext_views

from apps import TestAppConfig
from models import ModelA, ModelB


class ModelAAdmin(object):
    app_config = TestAppConfig()


class TestCommView(ext_views.AppConfigViewMixin, views.CommAdminView):
    pass


xadmin.site.register(ModelA, ModelAAdmin)
xadmin.site.register(ModelB)
xadmin.site.register(views.CommAdminView, TestCommView)

