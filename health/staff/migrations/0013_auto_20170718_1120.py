# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 02:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0012_auto_20170718_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='division',
            field=models.CharField(choices=[('new', '신규'), ('re', '재등록')], default='new', max_length=12, verbose_name='회원구분'),
        ),
        migrations.AddField(
            model_name='member',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 11, 20, 55, 31609), verbose_name='회원권종료일'),
        ),
        migrations.AlterField(
            model_name='member',
            name='sex',
            field=models.CharField(choices=[('M', '남자'), ('F', '여자')], max_length=12, null=True, verbose_name='성별'),
        ),
        migrations.AlterField(
            model_name='paymenthistory',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 17, 11, 20, 55, 33609), verbose_name='회원권종료일'),
        ),
    ]
