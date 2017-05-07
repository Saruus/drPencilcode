# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20170429_1814'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.RemoveField(
            model_name='dead',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='duplicate',
            name='myproject',
        ),
        migrations.RemoveField(
            model_name='sprite',
            name='myproject',
        ),
        migrations.DeleteModel(
            name='Dead',
        ),
        migrations.DeleteModel(
            name='Duplicate',
        ),
        migrations.DeleteModel(
            name='Sprite',
        ),
    ]
