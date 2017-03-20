# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0005_electricitytransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricitytransaction',
            name='customer_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
