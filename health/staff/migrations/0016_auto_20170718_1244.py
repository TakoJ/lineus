# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 03:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0015_auto_20170718_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 17, 12, 44, 38, 648158), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='비고란'),
        ),
        migrations.AlterField(
            model_name='member',
            name='registered_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='등록일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 12, 44, 38, 650159), verbose_name='회원권종료일'),
        ),
    ]