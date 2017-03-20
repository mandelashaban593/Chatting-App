# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0014_utilitytransaction_bill_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='beyon_sender',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
