# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0008_rwfwallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Smile_Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=40)),
                ('date_created', models.CharField(max_length=40)),
                ('expiry_date', models.CharField(max_length=40)),
            ],
        ),
    ]
