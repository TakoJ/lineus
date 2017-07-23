# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 06:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0021_auto_20170719_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='PT_status',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 18, 15, 7, 44, 606061), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 18, 15, 7, 44, 608062), verbose_name='회원권종료일'),
        ),
    ]
