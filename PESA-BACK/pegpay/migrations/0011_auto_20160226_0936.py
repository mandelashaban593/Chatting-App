# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0010_utilitytransaction_billtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='utilitytransaction',
            old_name='company_code',
            new_name='account_name',
        ),
        migrations.RenameField(
            model_name='utilitytransaction',
            old_name='customer_name',
            new_name='paymethod',
        ),
        migrations.RenameField(
            model_name='utilitytransaction',
            old_name='transaction_ref',
            new_name='recipient_phone',
        ),
        migrations.AddField(
            model_name='utilitytransaction',
            name='referencenum',
            field=models.CharField(max_length=130, blank=True),
        ),
        migrations.AddField(
            model_name='utilitytransaction',
            name='sender_message',
            field=models.CharField(max_length=130, blank=True),
        ),
    ]
