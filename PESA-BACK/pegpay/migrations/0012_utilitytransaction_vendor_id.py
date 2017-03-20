# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0011_auto_20160226_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='vendor_id',
            field=models.CharField(max_length=130, blank=True),
        ),
    ]
