# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_num', models.IntegerField()),
                ('account_detail', models.CharField(max_length=100)),
                ('balance', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_trans', models.CharField(max_length=100, choices=[(b'Credit', b'Credit'), (b'Debit', b'Debit'), (b'Transfer', b'Transfer')])),
                ('second_account', models.IntegerField(blank=True)),
                ('transaction_hashtag', models.CharField(max_length=100)),
                ('amount', models.IntegerField(max_length=100)),
                ('account_rel', models.ForeignKey(to='mngr.Account_details')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
