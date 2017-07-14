# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_auto_20170714_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pilates_GX_Basic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tuition', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='Pilates GX 수업당 수업비')),
            ],
        ),
        migrations.RenameModel(
            old_name='Pilates_GX',
            new_name='Pilates_GX_DependingNum',
        ),
    ]
