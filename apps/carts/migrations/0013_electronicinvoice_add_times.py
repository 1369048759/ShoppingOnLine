# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-27 00:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0012_electronicinvoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='electronicinvoice',
            name='add_times',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]