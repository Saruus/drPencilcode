# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20170430_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='bonus',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
