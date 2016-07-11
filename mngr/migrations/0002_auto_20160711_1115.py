# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mngr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_details',
            name='transaction_desc',
            field=models.CharField(default='nothing', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account_details',
            name='account_num',
            field=models.IntegerField(unique=True),
        ),
    ]
