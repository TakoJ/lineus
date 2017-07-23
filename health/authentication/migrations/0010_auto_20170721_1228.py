# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-21 03:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0009_auto_20170716_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fc_salary',
            name='refund',
        ),
        migrations.AddField(
            model_name='fc_salary',
            name='FC_refund',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=19, verbose_name='FC팀 총 환불'),
        ),
        migrations.AddField(
            model_name='fc_salary',
            name='personal_refund',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=19, verbose_name='개인 환불'),
        ),
        migrations.AlterField(
            model_name='fc_salary',
            name='commission',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='팀커미션'),
        ),
        migrations.AlterField(
            model_name='fc_salary',
            name='commission_rate',
            field=models.FloatField(blank=True, default=0.0, verbose_name='팀커미션 비율'),
        ),
        migrations.AlterField(
            model_name='fc_salary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='FC_Salary', to=settings.AUTH_USER_MODEL, verbose_name='이름'),
        ),
    ]
