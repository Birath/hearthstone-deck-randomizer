# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-13 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deck_randomizer', '0003_card_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='rarity',
            field=models.CharField(default='def', max_length=200),
            preserve_default=False,
        ),
    ]
