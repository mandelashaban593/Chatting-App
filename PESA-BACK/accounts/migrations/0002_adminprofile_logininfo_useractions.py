# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(default=False, max_length=100, blank=True, choices=[(b'UG', b'Uganda'), (b'KE', b'Kenya'), (b'TZ', b'Tanzania'), (b'RW', b'Rwanda')])),
                ('mobile_network', models.CharField(default=False, max_length=100, blank=True, choices=[(b'MTN', b'MTN Mobile Money'), (b'AIRTEL', b'Airtel Money'), (b'UTL', b'M-Sente')])),
                ('is_customer_care', models.BooleanField(default=False)),
                ('user', models.OneToOneField(related_name='admin_profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_audit_trail', 'View Audit Trails'),),
            },
        ),
        migrations.CreateModel(
            name='LoginInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField(auto_now_add=True)),
                ('user_agent', models.CharField(max_length=1000, null=True, blank=True)),
                ('remote_addr', models.GenericIPAddressField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_entry', models.ForeignKey(to='admin.LogEntry')),
                ('session', models.ForeignKey(to='accounts.LoginInfo')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
