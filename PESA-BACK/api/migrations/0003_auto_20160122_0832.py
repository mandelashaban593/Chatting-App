# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_paybillaccount_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='paybillaccount',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 8, 32, 8, 679629, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paybillaccount',
            name='vendorid',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
