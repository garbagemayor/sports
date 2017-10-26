# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Email(models.Model):
    addr = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()

