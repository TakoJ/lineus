# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 12:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0036_auto_20170705_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='PT_payment_amount',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True, verbose_name='PT결제금액'),
        ),
        migrations.AlterField(
            model_name='member',
            name='PT_payment_method',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='PT결제방식'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 4, 21, 28, 17, 733898), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='registered_date',
            field=models.DateField(default=django.utils.timezone.now, null=True, verbose_name='PT등록일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='registered_session',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='등록세션'),
        ),
    ]
