# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0044_auto_20170727_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locker',
            name='locker_amount',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='락카 금액'),
        ),
        migrations.AlterField(
            model_name='locker',
            name='locker_payment_method',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='락카결제방식'),
        ),
    ]