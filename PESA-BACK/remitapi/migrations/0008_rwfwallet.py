# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remitapi', '0007_auto_20151122_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='RWFWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.Wallet')),
            ],
            bases=('remitapi.wallet',),
        ),
    ]
