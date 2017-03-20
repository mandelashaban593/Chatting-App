# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paybillaccount',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 23, 11, 17, 30, 871126, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
