# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seccim_app', '0004_remove_speaker_sexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(default='', help_text='Descrição da palestra', max_length=1000, verbose_name='description'),
        ),
    ]
