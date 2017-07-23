# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 01:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0011_auto_20170717_1628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='PT_PT_registered_date',
            new_name='PT_registered_date',
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 10, 55, 35, 243546), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 10, 55, 35, 245547), verbose_name='회원권종료일'),
        ),
    ]
