# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_auto_20180517_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='css',
            name='color',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='css',
            name='size',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
