# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seccim_app', '0003_merge_20171017_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speaker',
            name='sexo',
        ),
    ]