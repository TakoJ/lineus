# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 05:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_auto_20170712_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='GX',
            field=models.BooleanField(default=False, verbose_name='GX 여부'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 11, 14, 48, 34, 259408), verbose_name='회원권종료일'),
        ),
    ]
