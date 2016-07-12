# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mngr', '0005_auto_20160712_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_details',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction_details',
            name='transaction_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
