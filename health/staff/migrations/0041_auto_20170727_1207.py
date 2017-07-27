# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0040_remove_member_period_locker'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='locker_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='락카 종료일'),
        ),
        migrations.AddField(
            model_name='member',
            name='locker_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='락카 시작일'),
        ),
    ]
