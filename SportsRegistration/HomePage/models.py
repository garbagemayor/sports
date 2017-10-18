# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Events(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=30)
    content = models.CharField(max_length=300)

class Sign(models.Model):
    id = models.IntegerField()
    userid = models.IntegerField()
    eventsid = models.IntegerField()
