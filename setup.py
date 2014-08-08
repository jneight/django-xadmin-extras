# coding=utf-8

import os
from setuptools import setup, find_packages
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

import xadmin_extras as xae

setup(
    name='django-xadmin-extras',
    version=xae.__version__,
    url='https://github.com/jneight/django-xadmin-extras',
    description="Extensions for django-xadmin",
    author=xae.__author__,
    author_email=xae.__email__,
    packages=find_packages(exclude=['tests', 'tests.*',]),
    include_package_data=True,
    license=xae.__license__,
    test_suite="tests",
    zip_safe=False,
)
