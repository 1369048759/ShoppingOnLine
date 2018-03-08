# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-12 09:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_help', '0005_auto_20171012_0713'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienceStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopname', models.CharField(max_length=50, verbose_name='店名')),
                ('group', models.IntegerField(choices=[(1, '东区'), (2, '南区'), (3, '西区'), (4, '北区')], default=1)),
                ('district', models.CharField(max_length=20, verbose_name='省份')),
                ('city', models.CharField(max_length=20, verbose_name='城市')),
                ('shopAddress', models.CharField(max_length=100, verbose_name='地址')),
                ('shopTel', models.CharField(max_length=11, verbose_name='联系电话')),
                ('add_times', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
        ),
        migrations.CreateModel(
            name='StopImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='stopImage/default.png', max_length=150, upload_to='stopImage/%Y%m', verbose_name='图片')),
                ('add_times', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_help.ExperienceStore', verbose_name='店铺')),
            ],
        ),
    ]
