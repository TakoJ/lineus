# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 03:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0042_auto_20170706_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='re_registered',
            field=models.BooleanField(default=False, verbose_name='재등록 여부'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 5, 12, 46, 27, 8244), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='registered_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='PT등록일'),
        ),
    ]
