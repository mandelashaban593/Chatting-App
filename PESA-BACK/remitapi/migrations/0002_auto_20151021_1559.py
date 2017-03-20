# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apitransaction',
            name='added',
        ),
        migrations.AddField(
            model_name='apitransaction',
            name='last_transaction',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
        migrations.RemoveField(
            model_name='apitransaction',
            name='app',
        ),
        migrations.AddField(
            model_name='apitransaction',
            name='app',
            field=models.ManyToManyField(related_name='remitapi_apitransaction_related', to='remitapi.App'),
        ),
    ]
