# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 03:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seccim_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='sexo',
            field=models.BooleanField(default=True, verbose_name='is_male'),
            preserve_default=False,
        ),
    ]