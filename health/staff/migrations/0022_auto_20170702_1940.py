# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 10:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0021_auto_20170702_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 1, 19, 40, 25, 48361), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=24, verbose_name='성명'),
        ),
    ]
