# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ipay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipaytransaction',
            name='credit',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='ipaytransaction',
            name='mnoreceipt',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ipaytransaction',
            name='recipient',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ipaytransaction',
            name='txncost',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
        ),
        migrations.AddField(
            model_name='ipaytransaction',
            name='txnref',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
