# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0010_auto_20180512_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='keyword',
            new_name='key',
        ),
        migrations.AddField(
            model_name='dialog',
            name='from_key',
            field=models.ForeignKey(null=True, to='dialog.Keyword'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='father_key',
            field=models.ForeignKey(null=True, to='dialog.Keyword'),
        ),
    ]
