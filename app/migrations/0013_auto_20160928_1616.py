# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20151016_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='abstraction',
        ),
        migrations.RemoveField(
            model_name='file',
            name='dataRepresentation',
        ),
        migrations.RemoveField(
            model_name='file',
            name='flowControl',
        ),
        migrations.RemoveField(
            model_name='file',
            name='logic',
        ),
        migrations.RemoveField(
            model_name='file',
            name='parallelism',
        ),
        migrations.RemoveField(
            model_name='file',
            name='score',
        ),
        migrations.RemoveField(
            model_name='file',
            name='synchronization',
        ),
        migrations.RemoveField(
            model_name='file',
            name='userInteractivity',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='abstraction',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='flowcontrol',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='interactivity',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='logic',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='paralel',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='representation',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='scoring',
        ),
        migrations.RemoveField(
            model_name='mastery',
            name='synchronization',
        ),
        migrations.AddField(
            model_name='file',
            name='art',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='control',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='move',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='operators',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='sound',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='text',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='art',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='control',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='move',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='operators',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='sound',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mastery',
            name='text',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
