# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-27 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0019_auto_20170627_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='등록횟수',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
