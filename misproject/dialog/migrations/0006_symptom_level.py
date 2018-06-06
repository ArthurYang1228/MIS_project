# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0005_symptom_symptom'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='level',
            field=models.CharField(choices=[(1, '蠻常見的'), (2, '還算聽過'), (3, '什麼鬼啦')], max_length=20, default=2),
        ),
    ]
