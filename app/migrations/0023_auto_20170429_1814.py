# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20170315_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='surname',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
