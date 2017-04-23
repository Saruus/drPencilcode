# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_survey'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='question2',
            field=models.CharField(default=50, max_length=50),
            preserve_default=False,
        ),
    ]
