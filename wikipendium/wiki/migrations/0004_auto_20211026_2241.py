# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-26 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0003_auto_20211026_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecontent',
            name='lang',
            field=models.CharField(default='en', max_length=2),
        ),
    ]
