# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0015_auto_20180519_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='playerid',
            field=models.CharField(max_length=500, default=' '),
        ),
    ]
