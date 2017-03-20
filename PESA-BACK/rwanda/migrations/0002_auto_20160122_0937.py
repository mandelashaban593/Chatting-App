# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rwanda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rwandatransaction',
            name='txnref',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
