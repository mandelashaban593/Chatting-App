# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remitapi', '0004_auto_20151030_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='KESWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.Wallet')),
            ],
            bases=('remitapi.wallet',),
        ),
        migrations.CreateModel(
            name='UGXWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.Wallet')),
            ],
            bases=('remitapi.wallet',),
        ),
        migrations.AddField(
            model_name='wallet',
            name='modified_by',
            field=models.ForeignKey(related_name='modified_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
