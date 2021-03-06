# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-05 04:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_str', models.CharField(blank=True, max_length=200)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Publication date')),
                ('text', models.TextField(blank=True, verbose_name=b'Tweet text')),
                ('screen_name', models.CharField(blank=True, max_length=200, verbose_name=b'@screen_name')),
                ('user_name', models.CharField(blank=True, max_length=200, verbose_name=b'User name')),
                ('outlet', models.CharField(blank=True, max_length=200, verbose_name=b'Outlet')),
                ('url', models.CharField(blank=True, max_length=200, verbose_name=b'Link to tweet')),
                ('url_user', models.CharField(blank=True, max_length=200, verbose_name=b'Link to user')),
                ('topic_0', models.CharField(blank=True, max_length=140)),
                ('topic_1', models.CharField(blank=True, max_length=140)),
                ('topic_2', models.CharField(blank=True, max_length=140)),
                ('topic_3', models.CharField(blank=True, max_length=140)),
                ('topic_4', models.CharField(blank=True, max_length=140)),
                ('topic_5', models.CharField(blank=True, max_length=140)),
                ('topic_6', models.CharField(blank=True, max_length=140)),
                ('topic_7', models.CharField(blank=True, max_length=140)),
                ('topic_8', models.CharField(blank=True, max_length=140)),
                ('topic_9', models.CharField(blank=True, max_length=140)),
            ],
        ),
    ]
