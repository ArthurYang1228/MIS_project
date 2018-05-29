# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0014_auto_20180518_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='response_type',
            field=models.IntegerField(default=1, choices=[(1, 'TEXT'), (2, 'CHOICE'), (3, 'PICTURE'), (4, 'FUNCTION')]),
        ),
    ]
