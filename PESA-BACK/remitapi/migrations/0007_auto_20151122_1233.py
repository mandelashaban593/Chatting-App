# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('remitapi', '0006_auto_20151113_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forex_percentage', models.DecimalField(default=4.5, max_digits=10, decimal_places=2)),
                ('transfer_fee_percentage', models.DecimalField(default=4.5, max_digits=10, decimal_places=2)),
                ('transfer_maximum_usd', models.DecimalField(default=500.0, max_digits=10, decimal_places=2)),
                ('transfer_minimum_usd', models.DecimalField(default=100.0, max_digits=10, decimal_places=2)),
                ('mtn_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('airtel_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('orange_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('tigo_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('safaricom_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('vodafone_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('general_network_charge', models.DecimalField(default=60.0, max_digits=10, decimal_places=2)),
                ('added', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('to_usd', models.DecimalField(default=2640.0, max_digits=10, decimal_places=2)),
                ('to_gbp', models.DecimalField(default=3974.0, max_digits=10, decimal_places=2)),
                ('to_eur', models.DecimalField(default=3256.0, max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=4)),
                ('name', models.CharField(max_length=40)),
                ('currency', models.CharField(unique=True, max_length=4)),
                ('added', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('dailing_code', models.CharField(default=256, max_length=5)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usd_to_rwf', models.DecimalField(default=688.0, max_digits=10, decimal_places=2)),
                ('gbp_to_rwf', models.DecimalField(default=1114.76, max_digits=10, decimal_places=2)),
                ('usd_to_ugx', models.DecimalField(default=2640.0, max_digits=10, decimal_places=2)),
                ('usd_to_kes', models.DecimalField(default=85.63, max_digits=10, decimal_places=2)),
                ('usd_to_tzs', models.DecimalField(default=1623.0, max_digits=10, decimal_places=2)),
                ('gbp_to_ugx', models.DecimalField(default=3974.19, max_digits=10, decimal_places=2)),
                ('gpb_to_kes', models.DecimalField(default=129.47, max_digits=10, decimal_places=2)),
                ('gpb_to_tzs', models.DecimalField(default=2453.0, max_digits=10, decimal_places=2)),
                ('transfer_limit_usd', models.DecimalField(default=500.0, max_digits=10, decimal_places=2)),
                ('transfer_minimum_usd', models.DecimalField(default=100.0, max_digits=10, decimal_places=2)),
                ('our_percentage', models.DecimalField(default=4.5, max_digits=10, decimal_places=2)),
                ('percentage_from_forex', models.DecimalField(default=4.5, max_digits=10, decimal_places=2)),
                ('added', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_rate', 'View Rates'), ('edit_rate', 'Edit Rates')),
            },
        ),
        migrations.AddField(
            model_name='charge',
            name='country',
            field=models.ForeignKey(blank=True, to='remitapi.Country', null=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
