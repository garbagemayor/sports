# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0009_sign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
