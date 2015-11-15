# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20151014_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='parallelization',
            new_name='parallelism',
        ),
    ]
