# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 06:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0020_auto_20170719_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='Membership_status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='PT_status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 18, 15, 2, 24, 447005), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='re_registered',
            field=models.BooleanField(default=False, verbose_name='PT재등록 여부'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 18, 15, 2, 24, 449006), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='refundhistory',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to='staff.PaymentHistory'),
        ),
    ]
