# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 06:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0023_auto_20170719_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='division',
            field=models.CharField(max_length=12, null=True, verbose_name='Fitness/Pilates 구분'),
        ),
        migrations.AlterField(
            model_name='member',
            name='PT_registered_date',
            field=models.DateField(blank=True, null=True, verbose_name='PT등록일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 20, 15, 14, 15, 2772), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='division',
            field=models.CharField(max_length=12, null=True, verbose_name='회원권/Fitness/Pilates 구분'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 20, 15, 14, 15, 5774), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='refundhistory',
            name='division',
            field=models.CharField(max_length=12, null=True, verbose_name='회원권/Fitness/Pilates 구분'),
        ),
    ]