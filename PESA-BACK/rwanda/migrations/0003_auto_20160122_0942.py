# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rwanda', '0002_auto_20160122_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rwandatransaction',
            name='txnref',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
