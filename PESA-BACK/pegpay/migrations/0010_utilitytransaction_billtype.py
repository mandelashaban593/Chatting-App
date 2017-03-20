# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0009_auto_20151113_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='billtype',
            field=models.CharField(max_length=130, blank=True),
        ),
    ]
