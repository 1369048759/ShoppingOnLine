# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-23 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cartsforuser_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartsforuser',
            name='cart',
            field=models.CharField(max_length=100000, verbose_name='购物车'),
        ),
    ]
