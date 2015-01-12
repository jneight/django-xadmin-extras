# coding=utf-8

""":synapsis: Extend xadmin views
* AppConfigViewMixin

"""

import sys
import copy

from django.utils.datastructures import SortedDict
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from xadmin import views
from xadmin.util import sortkeypicker
from xadmin.layout import FormHelper, Layout, Fieldset, TabHolder, Container, Column, Col, Field


class AppConfigViewMixin(object):
    """Using django new AppConfig and extra properties,
    (see apps.py AdminAppMixin), this extension allow to add custom entries
    for each menu without using models.

    See apps.AdminAppMixin for menu syntax

    """
    def get_apps_menu(self):
        """Temporal code, will change to apps.get_app_configs() for django 1.7

        Generate a initial menu list using the AppsConfig registered
        """
        menu = {}
        for model, model_admin in self.admin_site._registry.items():
            if hasattr(model_admin, 'app_config'):
                if model_admin.app_config.has_menu_permission(obj=self.user):
                    menu.update({
                        'app:' + model_admin.app_config.name: {
                        'title': model_admin.app_config.verbose_name,
                        'menus': model_admin.app_config.init_menu(),
                        'first_icon': model_admin.app_config.icon}})
        return menu

    @views.filter_hook
    def get_nav_menu(self):
        """Method to generate the menu"""
        _menu = self.get_site_menu()
        if _menu:
            site_menu = list(_menu)
        else:
            site_menu = []
        had_urls = []

        def get_url(menu, had_urls):
            if 'url' in menu:
                had_urls.append(menu['url'])
            if 'menus' in menu:
                for m in menu['menus']:
                    get_url(m, had_urls)
        get_url({'menus': site_menu}, had_urls)

        # get base menu with apps already configurated
        nav_menu = SortedDict(self.get_apps_menu())

        for model, model_admin in self.admin_site._registry.items():
            if getattr(model_admin, 'hidden_menu', False):
                continue
            app_config = getattr(model_admin, 'app_config', None)
            app_label = app_config.name if app_config else model._meta.app_label
            model_dict = {
                'title': unicode(capfirst(model._meta.verbose_name_plural)),
                'url': self.get_model_url(model, "changelist"),
                'icon': self.get_model_icon(model),
                'perm': self.get_model_perm(model, 'view'),
                'order': model_admin.order,
            }
            if model_dict['url'] in had_urls:
                continue
            app_key = "app:%s" % app_label
            if app_key in nav_menu:
                nav_menu[app_key]['menus'].append(model_dict)
            else:
                # first time the app is seen
                # Find app title
                if app_config:
                    app_title = model_admin.app_config.verbose_name
                else:
                    app_title = unicode(app_label.title())
                    if app_label.lower() in self.apps_label_title:
                        app_title = self.apps_label_title[app_label.lower()]
                    else:
                        mods = model.__module__.split('.')
                        if len(mods) > 1:
                            mod = '.'.join(mods[0:-1])
                            if mod in sys.modules:
                                mod = sys.modules[mod]
                                if 'verbose_name' in dir(mod):
                                    app_title = getattr(mod, 'verbose_name')
                                elif 'app_title' in dir(mod):
                                    app_title = getattr(mod, 'app_title')

                nav_menu[app_key] = {
                    'title': app_title,
                    'menus': [model_dict],
                }

            app_menu = nav_menu[app_key]
            if ('first_icon' not in app_menu or
                    app_menu['first_icon'] == self.default_model_icon) and model_dict.get('icon'):
                app_menu['first_icon'] = model_dict['icon']
            if 'first_url' not in app_menu and model_dict.get('url'):
                app_menu['first_url'] = model_dict['url']
        # after app menu is done, join it to the site menu
        nav_menu = nav_menu.values()
        site_menu.extend(nav_menu)
        for menu in site_menu:
            menu['menus'].sort(key=sortkeypicker(['order', 'title']))
        site_menu.sort(key=lambda x: x['title'])
        return site_menu


class MultipleFormsMixin(object):
    form_add = None
    layout_add = None

    def _doing_add(self):
        obj = self.get_form_datas().get('instance', None)
        if not obj or obj.pk is obj._meta.pk.get_default():
            return True
        return False

    @views.filter_hook
    def get_model_form(self, **kwargs):
        if self._doing_add() and self.form_add is not None:
            return self.form_add
        return super(MultipleFormsMixin, self).get_model_form(**kwargs)

    @views.filter_hook
    def get_form_layout(self):
        if not self._doing_add() or self.form_layout_add is None:
            return super(MultipleFormsMixin, self).get_form_layout()
        layout = copy.deepcopy(self.form_layout_add)
        fields = self.form_obj.fields.keys()
        return self._get_form_layout(layout, fields)

    def _get_form_layout(self, layout, fields):
        if layout is None:
            layout = Layout(Container(Col('full',
                Fieldset("", *fields, css_class="unsort no_title"), horizontal=True, span=12)
                ))
        elif type(layout) in (list, tuple) and len(layout) > 0:
            if isinstance(layout[0], Column):
                fs = layout
            elif isinstance(layout[0], (Fieldset, TabHolder)):
                fs = (Col('full', *layout, horizontal=True, span=12),)
            else:
                fs = (Col('full', Fieldset("", *layout, css_class="unsort no_title"), horizontal=True, span=12),)
            layout = Layout(Container(*fs))
            rendered_fields = [i[1] for i in layout.get_field_names()]
            container = layout[0].fields
            other_fieldset = Fieldset(_(u'Other Fields'), *[f for f in fields if f not in rendered_fields])
            if len(other_fieldset.fields):
                if len(container) and isinstance(container[0], Column):
                    container[0].fields.append(other_fieldset)
                else:
                    container.append(other_fieldset)
        return layout

    @views.filter_hook
    def get_readonly_fields(self):
        if self._doing_add() and self.form_add is not None:
            return []
        return super(MultipleFormsMixin, self).get_readonly_fields()

