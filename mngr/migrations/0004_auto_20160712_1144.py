# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mngr', '0003_auto_20160711_1855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction_details',
            old_name='second_account',
            new_name='receiving_account',
        ),
        migrations.RenameField(
            model_name='transaction_details',
            old_name='transaction_hashtag',
            new_name='transaction_hashtags',
        ),
    ]
