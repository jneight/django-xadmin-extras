# coding=utf-8

""" :synopsis: Utilities """


from mail_factory import factory
from django.utils import six

def registered_mails_names():
    if hasattr(factory, '_registry'):
        for k, v in six.iteritems(factory._registry):
            yield k, v.__name__
        return
    else:
        for k, v in six.iteritems(factory.mail_map):
            yield k, v.__name__
        return

