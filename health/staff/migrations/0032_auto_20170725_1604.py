# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0031_merge_20170725_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(blank=True, verbose_name='회원권종료일'),
        ),
    ]
