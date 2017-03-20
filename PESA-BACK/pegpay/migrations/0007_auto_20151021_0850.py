# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0006_auto_20151020_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricitytransaction',
            name='customer_email',
            field=models.EmailField(max_length=75, blank=True),
        ),
    ]
