# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mngr', '0002_auto_20160711_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_details',
            name='second_account',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
