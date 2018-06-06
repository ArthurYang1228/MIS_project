# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0008_auto_20180511_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='level',
            field=models.CharField(max_length=20, default='2', choices=[('0', '沒毛病吧'), ('1', '蠻常見的'), ('2', '還算聽過'), ('3', '什麼鬼啦')]),
        ),
    ]
