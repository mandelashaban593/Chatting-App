# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firebase_cloud_msging', '0002_auto_20161018_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifsclient',
            name='client_name',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
