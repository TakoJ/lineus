# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 03:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0010_auto_20170717_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 16, 12, 38, 46, 969690), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 16, 12, 38, 46, 971095), verbose_name='회원권종료일'),
        ),
    ]