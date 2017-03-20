# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MtnTransaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('response', jsonfield.fields.JSONField()),
                ('phonenumber', models.CharField(max_length=20)),
            ],
            bases=('remitapi.app',),
        ),
    ]
