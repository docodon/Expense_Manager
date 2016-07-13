# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mngr', '0006_auto_20160712_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_details',
            name='transaction_hashtags',
            field=tagging.fields.TagField(max_length=255, null=True, blank=True),
        ),
    ]
