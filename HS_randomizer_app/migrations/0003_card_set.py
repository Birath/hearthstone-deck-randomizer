# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-11 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HS_randomizer_app', '0002_card_dbfid'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='set',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
