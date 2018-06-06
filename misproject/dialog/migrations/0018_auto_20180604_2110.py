# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0017_auto_20180601_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='division',
            field=models.CharField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='name_English',
            field=models.CharField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='organ',
            field=models.CharField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='prevention',
            field=models.CharField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='symptom',
            name='symptom',
            field=models.CharField(max_length=600, blank=True),
        ),
    ]
