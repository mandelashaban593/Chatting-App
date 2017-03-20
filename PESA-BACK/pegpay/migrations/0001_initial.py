# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('company_code', models.CharField(max_length=130, blank=True)),
                ('transaction_ref', models.CharField(max_length=130, blank=True)),
                ('customer_name', models.CharField(max_length=130, blank=True)),
                ('paid_by', models.CharField(max_length=130, blank=True)),
            ],
            bases=('remitapi.app',),
        ),
    ]
