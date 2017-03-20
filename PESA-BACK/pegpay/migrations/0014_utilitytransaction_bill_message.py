# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0013_utilitytransaction_mobile_response_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitytransaction',
            name='bill_message',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
