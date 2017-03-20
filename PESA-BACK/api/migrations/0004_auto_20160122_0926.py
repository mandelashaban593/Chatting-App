# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20160122_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paybillaccount',
            name='send_date',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
