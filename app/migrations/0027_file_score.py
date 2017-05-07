# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20170430_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='score',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
