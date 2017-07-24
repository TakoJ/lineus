# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 06:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_auto_20170711_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='unitprice',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='1회세션단가'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 10, 15, 34, 39, 614378), verbose_name='회원권종료일'),
        ),
    ]