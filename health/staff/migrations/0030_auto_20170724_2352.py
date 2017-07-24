# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0029_auto_20170724_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='refundhistory',
            name='fees',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='수수료'),
        ),
        migrations.AddField(
            model_name='refundhistory',
            name='refund',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True, verbose_name='환불금액'),
        ),
        migrations.AlterField(
            model_name='refundhistory',
            name='refund_amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='총합'),
        ),
    ]