# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-11 23:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service_help', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicehelp',
            name='image',
        ),
    ]
