# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 03:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0033_auto_20170726_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pil_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth', models.DateField(blank=True, help_text='Ex) 1980-06-30', null=True, verbose_name='생년월일')),
                ('division', models.CharField(blank=True, max_length=12, null=True, verbose_name='PT 구분')),
                ('Pil_registered_session', models.CharField(blank=True, max_length=24, verbose_name='Pilates 등록세션')),
                ('Pil_payment_amount', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='Pilates 결제금액')),
                ('Pil_payment_method', models.CharField(blank=True, max_length=12, verbose_name='Pilates 결제방식')),
                ('Pil_unitprice', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Pil_1회세션단가')),
                ('Pil_period_PT', models.CharField(blank=True, max_length=12, null=True, verbose_name='Pil_강습기간')),
                ('Pil_registered_date', models.DateField(blank=True, verbose_name='Pilates 등록일')),
                ('Num', models.IntegerField(default=0)),
                ('Trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Pil_Trainer', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(max_length=12, on_delete=django.db.models.deletion.CASCADE, related_name='Pil_History', to='staff.Member', verbose_name='성명')),
            ],
        ),
        migrations.AlterField(
            model_name='history',
            name='division',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='PT 구분'),
        ),
    ]
