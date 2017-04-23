# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20170312_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='question2',
            field=models.CharField(default=10, max_length=10),
            preserve_default=False,
        ),
    ]
