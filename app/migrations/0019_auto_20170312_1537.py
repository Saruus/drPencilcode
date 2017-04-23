# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170312_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='question1',
            new_name='question1a',
        ),
        migrations.RenameField(
            model_name='survey',
            old_name='question2',
            new_name='question1b',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='question3',
        ),
        migrations.AddField(
            model_name='survey',
            name='question2a',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question2b',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question2c',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question2d',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
