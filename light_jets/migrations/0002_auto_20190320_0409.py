# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-20 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('light_jets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('tracking_id', models.AutoField(primary_key=True, serialize=False)),
                ('track_datetime', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('longitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('elevation', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracking', to='light_jets.Product', unique=True)),
            ],
            options={
                'db_table': 'tracking',
                'verbose_name': 'Tracking Details',
                'verbose_name_plural': 'Tracking Details',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tracking',
            unique_together=set([('track_datetime', 'latitude', 'longitude')]),
        ),
    ]
