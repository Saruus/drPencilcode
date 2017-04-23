# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_survey_question2'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='question3',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='survey',
            name='question1',
            field=models.CharField(max_length=10),
        ),
    ]
