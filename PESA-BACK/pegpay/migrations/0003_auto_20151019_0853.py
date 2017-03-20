# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '__first__'),
        ('pegpay', '0002_auto_20151014_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterTransaction',
            fields=[
                ('app_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.App')),
                ('customer_ref', models.CharField(max_length=130, blank=True)),
                ('company_code', models.CharField(max_length=130, blank=True)),
                ('transaction_ref', models.CharField(max_length=130, blank=True)),
                ('customer_name', models.CharField(max_length=130, blank=True)),
                ('paid_by', models.CharField(max_length=130, blank=True)),
                ('customer_phone', models.CharField(max_length=130, blank=True)),
                ('sender_message', models.CharField(max_length=130, blank=True)),
                ('area', models.CharField(max_length=130, blank=True)),
            ],
            options={
            },
            bases=('remitapi.app',),
        ),
        migrations.RenameModel(
            old_name='PegpayTransaction',
            new_name='UtilityTransaction',
        ),
    ]
