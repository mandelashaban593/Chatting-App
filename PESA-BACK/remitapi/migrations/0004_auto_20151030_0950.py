# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0003_auto_20151030_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usdwallet',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='usdwallet',
            name='debit',
        ),
        migrations.AddField(
            model_name='wallet',
            name='added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='wallet',
            name='credit',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='wallet',
            name='debit',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
        ),
    ]
