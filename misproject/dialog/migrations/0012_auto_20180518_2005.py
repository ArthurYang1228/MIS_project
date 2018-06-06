# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0011_auto_20180518_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='from_key',
            field=models.ForeignKey(default=None, to='dialog.Keyword', null=True),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='father_key',
            field=models.ForeignKey(default=None, to='dialog.Keyword', null=True),
        ),
    ]
