# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_survey_question6'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='question3a',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question3b',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question3c',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question4',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='question5',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
