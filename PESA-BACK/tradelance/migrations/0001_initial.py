# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0008_rwfwallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='TlanceTransaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('api', models.CharField(max_length=130, blank=True)),
            ],
            bases=('remitapi.app',),
        ),
    ]
