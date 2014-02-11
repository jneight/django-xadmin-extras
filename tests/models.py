# coding=utf-8

from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=1)

    class Meta:
        app_label = 'tests'


class ModelB(models.Model):
    name = models.CharField(max_length=1)

    class Meta:
        app_label = 'tests'


