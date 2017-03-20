# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaybillAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', jsonfield.fields.JSONField(blank=True)),
                ('referencenumber', models.CharField(max_length=100)),
                ('location', models.CharField(default=b'', max_length=100)),
                ('billtype', models.IntegerField(default=1)),
            ],
        ),
    ]
