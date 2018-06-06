# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dialog', '0003_auto_20180416_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('name_English', models.CharField(max_length=100, blank=True)),
                ('division', models.CharField(max_length=100, blank=True)),
                ('organ', models.CharField(max_length=100, blank=True)),
                ('introduction', models.TextField(blank=True)),
                ('prevention', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='keyword',
            name='response_type',
            field=models.CharField(choices=[(1, 'TEXT'), (2, 'CHOICE'), (3, 'PICTURE')], max_length=5, default=1),
        ),
    ]
