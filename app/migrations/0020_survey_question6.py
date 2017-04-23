# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20170312_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='question6',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
