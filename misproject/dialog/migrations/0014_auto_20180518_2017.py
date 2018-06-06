# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0013_auto_20180518_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='from_key',
            field=models.ForeignKey(null=True, default=None, blank=True, to='dialog.Keyword'),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='father_key',
            field=models.ForeignKey(null=True, default=None, blank=True, to='dialog.Keyword'),
        ),
    ]
