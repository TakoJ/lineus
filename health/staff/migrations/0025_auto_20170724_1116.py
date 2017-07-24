# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 02:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0024_auto_20170721_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='division',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Fitness/Pilates 구분'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 23, 11, 16, 28, 744937), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 23, 11, 16, 28, 749942), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='refundhistory',
            name='division',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='회원권/Fitness/Pilates 구분'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='PT_registered_date',
            field=models.DateField(blank=True, null=True, verbose_name='해당PT등록일'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='GX명수'),
        ),
    ]