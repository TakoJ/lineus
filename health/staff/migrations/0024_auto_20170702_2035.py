# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 11:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0023_auto_20170702_1955'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='period_fitness',
            new_name='period_Fitness',
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 1, 20, 35, 22, 998462), verbose_name='회원권종료일'),
        ),
    ]
