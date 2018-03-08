# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-26 23:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_auto_20171025_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='city',
        ),
        migrations.RemoveField(
            model_name='area',
            name='province',
        ),
        migrations.RemoveField(
            model_name='city',
            name='province',
        ),
        migrations.RemoveField(
            model_name='provincearea',
            name='province',
        ),
        migrations.DeleteModel(
            name='Area',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Province',
        ),
        migrations.DeleteModel(
            name='ProvinceArea',
        ),
    ]
