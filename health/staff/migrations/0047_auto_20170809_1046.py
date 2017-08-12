# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 01:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0046_paymenthistory_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locker',
            name='locker_end_date',
        ),
        migrations.RemoveField(
            model_name='locker',
            name='locker_start_date',
        ),
        migrations.AddField(
            model_name='locker',
            name='G_locker_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='골프락카 종료일'),
        ),
        migrations.AddField(
            model_name='locker',
            name='G_locker_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='골프락카 시작일'),
        ),
        migrations.AddField(
            model_name='locker',
            name='H_locker_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='헬스락카 종료일'),
        ),
        migrations.AddField(
            model_name='locker',
            name='H_locker_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='헬스락카 시작일'),
        ),
    ]
