# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '__first__'),
        ('pegpay', '0004_auto_20151019_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityTransaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('customer_type', models.CharField(max_length=130)),
                ('payment_type', models.CharField(max_length=130)),
                ('sender_message', models.CharField(max_length=130, blank=True)),
                ('customer_ref', models.CharField(max_length=50)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=50)),
                ('paid_by', models.CharField(max_length=50)),
                ('customer_email', models.EmailField(max_length=75, blank=True)),
                ('company_code', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=('remitapi.app',),
        ),
    ]
