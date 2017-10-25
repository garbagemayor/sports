# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)    
    mobile = models.CharField(max_length=30, null=True)
    fullname = models.CharField(max_length=30, null=True)
    classnumber = models.CharField(max_length=30, null=True)
    authority = models.IntegerField(default=0)            #权限 默认无权限为0，普通管理员为1，超管为2
    email = models.CharField(max_length=30, null=True)

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
    status = models.IntegerField(default=1)     #0 未报名 1 等待审核 2 报名成功
    prize = models.CharField(max_length=30, null=True)
