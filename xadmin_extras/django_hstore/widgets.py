# coding=utf-8

from __future__ import unicode_literals, absolute_import

from django import forms
from django.contrib.admin.templatetags.admin_static import static

from django_hstore.widgets import BaseAdminHStoreWidget


class XAdminHStoreWidget(BaseAdminHStoreWidget):
    admin_style = 'xadmin'

    @property
    def media(self):
        # load underscore from CDNJS (popular javascript content delivery network)
        external_js = [
            "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min.js"
        ]

        internal_js = [
            "django-hstore/hstore-xadmin-widget.js"
        ]

        js = external_js + [static("xadmin/vendor/%s" % path) for path in internal_js]

        return forms.Media(js=js)
