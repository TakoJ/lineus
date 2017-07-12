# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FC_Personal_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='FC 개인매출')),
                ('personeel', models.IntegerField(null=True, verbose_name='인원')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
            ],
        ),
        migrations.CreateModel(
            name='FC_Team_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='FC팀 매출')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
            ],
        ),
        migrations.CreateModel(
            name='FC_Teamleader_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='팀매출')),
                ('personeel', models.IntegerField(null=True, verbose_name='인원')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
            ],
        ),
        migrations.CreateModel(
            name='Fitness_Personal_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Fitness 개인매출')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
                ('tuition_commission', models.IntegerField(default=0, verbose_name='수업료 비율')),
            ],
        ),
        migrations.CreateModel(
            name='Fitness_Teamledaer_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Fitness팀 매출')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
                ('tuition_commission', models.IntegerField(default=50, verbose_name='수업료 비율')),
            ],
        ),
        migrations.CreateModel(
            name='Pilates_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Pilates 개인매출')),
                ('tuition_commission', models.FloatField(default=30.0, verbose_name='수업료 비율')),
                ('tuition', models.DecimalField(blank=True, decimal_places=0, default=20000, max_digits=10, null=True, verbose_name='수업당 수업비')),
            ],
        ),
        migrations.CreateModel(
            name='Pilates_Teamleader_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.DecimalField(decimal_places=0, default=0, max_digits=19, verbose_name='Pilates팀 매출')),
                ('commission', models.FloatField(default=0.0, verbose_name='커미션')),
                ('tuition', models.DecimalField(blank=True, decimal_places=0, default=30000, max_digits=10, null=True, verbose_name='수업당 수업비')),
            ],
        ),
    ]
