# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-29 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0013_electronicinvoice_add_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electronicinvoice',
            name='inv_payee',
            field=models.CharField(default='', max_length=50, verbose_name='姓名'),
        ),
    ]