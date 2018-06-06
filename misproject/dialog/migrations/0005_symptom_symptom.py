# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0004_auto_20180508_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='symptom',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
