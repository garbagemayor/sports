# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0002_auto_20171018_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='status',
            field=models.CharField(default=123, max_length=20),
            preserve_default=False,
        ),
    ]
