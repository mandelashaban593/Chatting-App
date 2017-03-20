# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0008_rwfwallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='RwandaTransaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('response', jsonfield.fields.JSONField()),
                ('phonenumber', models.CharField(max_length=20)),
                ('txnref', models.CharField(max_length=50)),
                ('credit', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('txncost', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
            ],
            bases=('remitapi.app',),
        ),
    ]
