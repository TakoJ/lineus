# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 14:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0038_auto_20170705_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='registered_date',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='PT등록일'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='used_session',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='사용한 세션'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 4, 23, 26, 36, 845085), verbose_name='회원권종료일'),
        ),
    ]
