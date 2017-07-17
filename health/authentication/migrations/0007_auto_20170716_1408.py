# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 05:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_fitness_salary_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pilates_Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(null=True)),
                ('date', models.DateField(verbose_name='날짜')),
                ('team_sales', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=19, verbose_name='팀 매출')),
                ('personal_sales', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=19, verbose_name='개인 매출')),
                ('basic_salary', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='기본급')),
                ('commission_rate', models.FloatField(blank=True, default=0.0, verbose_name='커미션 비율')),
                ('commission', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='커미션')),
                ('GX_commission', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='GX 커미션')),
                ('PT_commission_rate', models.FloatField(blank=True, default=0.0, verbose_name='PT 커미션 비율')),
                ('PT_commission', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='PT 커미션')),
                ('total', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=12, verbose_name='합계')),
                ('refund', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, null=True, verbose_name='환불 합계')),
                ('salary', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=10, verbose_name='월급')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pilates_Salary', to=settings.AUTH_USER_MODEL, verbose_name='이름')),
            ],
        ),
        migrations.AlterModelOptions(
            name='fitness_salary',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='fitness_salary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fitness_Salary', to=settings.AUTH_USER_MODEL, verbose_name='이름'),
        ),
    ]
