# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0007_auto_20151021_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricitytransaction',
            name='customer_email',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
