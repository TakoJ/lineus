# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 03:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0014_auto_20170718_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 12, 31, 33, 985087), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 12, 31, 33, 989091), verbose_name='회원권종료일'),
        ),
    ]
