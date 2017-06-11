# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-11 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfers', '0002_auto_20170519_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surfer',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email address already exists.'}, max_length=150, unique=True, verbose_name='email address'),
        ),
    ]
