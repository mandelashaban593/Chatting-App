# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pegpay', '0003_auto_20151019_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watertransaction',
            name='area',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='company_code',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='customer_name',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='customer_phone',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='customer_ref',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='paid_by',
            field=models.CharField(max_length=130),
        ),
        migrations.AlterField(
            model_name='watertransaction',
            name='transaction_ref',
            field=models.CharField(max_length=130),
        ),
    ]
