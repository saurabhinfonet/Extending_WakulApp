# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_remove_outlet_geojson'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='names_other',
            field=models.CharField(blank=True, max_length=500, verbose_name=b'Other names (comma-separated)'),
        ),
    ]