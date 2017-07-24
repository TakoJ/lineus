# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 12:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_auto_20170718_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenthistory',
            name='division',
            field=models.CharField(max_length=12, null=True, verbose_name='회원권/PT 구분'),
        ),
        migrations.AlterField(
            model_name='member',
            name='division',
            field=models.CharField(default='new', max_length=12, verbose_name='회원구분'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 17, 21, 10, 23, 689583), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='sex',
            field=models.CharField(max_length=12, null=True, verbose_name='성별'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 21, 10, 23, 694106), verbose_name='회원권종료일'),
        ),
    ]