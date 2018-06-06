# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0007_auto_20180511_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='division',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='level',
            field=models.CharField(default='2', max_length=20, choices=[('1', '蠻常見的'), ('2', '還算聽過'), ('3', '什麼鬼啦')]),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='name_English',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='organ',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='prevention',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='symptom',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
