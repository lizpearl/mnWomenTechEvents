# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('techCalendar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='created_datetime',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 11, 26, 22, 212006), verbose_name=b'created_datetime'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='source',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
