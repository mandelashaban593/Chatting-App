# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firebase_cloud_msging', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifsclient',
            name='api_key',
            field=models.CharField(unique=True, max_length=300),
        ),
    ]
