# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0002_auto_20180323_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='response_type',
            field=models.IntegerField(max_length=5, default=1, choices=[(1, 'TEXT'), (2, 'CHOICE'), (3, 'PICTURE')]),
        ),
    ]
