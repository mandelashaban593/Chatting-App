# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remitapi', '0002_auto_20151021_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('currency', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='USDWallet',
            fields=[
                ('wallet_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='remitapi.Wallet')),
                ('credit', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('debit', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
            ],
            bases=('remitapi.wallet',),
        ),
        migrations.AddField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
