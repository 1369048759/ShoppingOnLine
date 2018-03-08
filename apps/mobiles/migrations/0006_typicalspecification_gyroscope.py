# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-17 09:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobiles', '0005_typicalspecification_wifi'),
    ]

    operations = [
        migrations.AddField(
            model_name='typicalspecification',
            name='gyroscope',
            field=models.IntegerField(choices=[(1, '支持'), (2, '不支持')], default=1, verbose_name='陀螺仪'),
        ),
    ]