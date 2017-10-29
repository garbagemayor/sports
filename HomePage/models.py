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
    authority = models.IntegerField(default=0)  # 权限 默认无权限为0，普通管理员为1，超管为2
    email = models.CharField(max_length=30, null=True)
    certification_type = models.IntegerField(default=0)  # 证件类型 默认0为身份证，护照为1
    certification_id = models.CharField(max_length=30)
    student_number = models.CharField(max_length=30)
    birthday = models.DateField(unique_for_date=True)
    CLOTH_SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Middle'),
        ('L', 'Large'),
    )
    cloth_size = models.CharField(max_length=1, null=True, choices=CLOTH_SIZE_CHOICES)
    room_address = models.CharField(max_length=30, null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, null=False, choices=GENDER_CHOICES)
    degree = models.IntegerField(null=True)  # 攻读学位 0为本科 1为研究生


class Events(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=300, null=True)


class Sign(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.IntegerField()
    eventsid = models.IntegerField()
    status = models.IntegerField(default=1)  # 0 未报名 1 等待审核 2 报名成功
    prize = models.CharField(max_length=30, null=True)
    time = models.DateTimeField(default=timezone.now)
