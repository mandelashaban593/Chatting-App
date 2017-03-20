# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rwanda', '0003_auto_20160122_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='rwandatransaction',
            name='sendername',
            field=models.CharField(default=b'Remit', max_length=50),
        ),
        migrations.AddField(
            model_name='rwandatransaction',
            name='senderreason',
            field=models.CharField(default=b'From Remit', max_length=50),
        ),
    ]
