# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 06:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0030_auto_20170704_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='user',
            field=models.CharField(max_length=12, verbose_name='성명'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 3, 15, 11, 41, 298427), verbose_name='회원권종료일'),
        ),
    ]
