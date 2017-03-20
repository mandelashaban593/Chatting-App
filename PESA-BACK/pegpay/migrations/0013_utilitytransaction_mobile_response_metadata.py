# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0012_utilitytransaction_vendor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='mobile_response_metadata',
            field=models.TextField(default=False, blank=True),
        ),
    ]
