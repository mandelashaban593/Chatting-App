# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0015_utilitytransaction_beyon_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='beyon_transid',
            field=models.CharField(max_length=130, blank=True),
        ),
    ]
