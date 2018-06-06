# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0009_auto_20180512_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='content',
            field=models.TextField(default=' '),
        ),
    ]
