# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0006_symptom_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='level',
            field=models.CharField(default=2, choices=[('1', '蠻常見的'), ('2', '還算聽過'), ('3', '什麼鬼啦')], max_length=20),
        ),
    ]
