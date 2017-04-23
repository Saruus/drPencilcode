# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20170312_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='date',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='surname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
