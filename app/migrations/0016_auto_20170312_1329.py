# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_survey_question2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='question2',
        ),
        migrations.AlterField(
            model_name='survey',
            name='question1',
            field=models.CharField(max_length=100),
        ),
    ]
