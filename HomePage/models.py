# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    classNumber = models.CharField(max_length=30, null=True)

class Events(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    date = models.DateTimeField(default = timezone.now)
    content = models.CharField(max_length=300, null=True)

class Sign(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    eventsid = models.IntegerField()
    result = models.IntegerField(null=True)


