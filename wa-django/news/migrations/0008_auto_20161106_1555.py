# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 04:55
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_outlet_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outlet',
            name='place',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]
