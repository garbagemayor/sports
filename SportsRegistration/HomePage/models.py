# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
<<<<<<< HEAD
    id = models.IntegerField(primary_key=True)
=======
    id = models.IntegerField()
>>>>>>> ccabf273b7190cc73584262f30b6394e7f85573c
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Events(models.Model):
<<<<<<< HEAD
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=20)
    date = models.DateTimeField(default = timezone.now)
    content = models.CharField(max_length=300, null=True)

class Sign(models.Model):
    id = models.IntegerField(primary_key=True)
=======
    id = models.IntegerField()
    name = models.CharField(max_length=30)
    content = models.CharField(max_length=300)

class Sign(models.Model):
    id = models.IntegerField()
>>>>>>> ccabf273b7190cc73584262f30b6394e7f85573c
    userid = models.IntegerField()
    eventsid = models.IntegerField()
