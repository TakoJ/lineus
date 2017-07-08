# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 03:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0041_auto_20170705_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='period_PT',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='강습기간'),
        ),
        migrations.AddField(
            model_name='history',
            name='unitprice',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='1회세션단가'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 5, 12, 11, 41, 945310), verbose_name='회원권종료일'),
        ),
    ]