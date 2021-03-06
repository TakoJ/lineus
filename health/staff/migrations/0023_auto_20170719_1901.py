# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 10:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0022_auto_20170719_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='refundhistory',
            name='date',
            field=models.DateField(null=True, verbose_name='결제일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 18, 19, 1, 4, 323698), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 18, 19, 1, 4, 328701), verbose_name='회원권종료일'),
        ),
    ]
