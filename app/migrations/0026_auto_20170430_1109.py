# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_file_bonus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='project',
            name='dashboard',
        ),
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Mastery',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
