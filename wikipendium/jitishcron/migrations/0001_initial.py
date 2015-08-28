# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskExecution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('key', models.CharField(max_length=256)),
                ('execution_number', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='taskexecution',
            unique_together=set([('key', 'execution_number')]),
        ),
    ]
