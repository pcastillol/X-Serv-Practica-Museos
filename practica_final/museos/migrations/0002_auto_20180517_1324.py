# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='css',
            name='color',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AlterField(
            model_name='css',
            name='titulo',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='css',
            name='user',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='barrio',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='museo',
            name='contacto',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='museo',
            name='distrito',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='museo',
            name='enlace',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='museo',
            name='nombre',
            field=models.CharField(max_length=256),
        ),
    ]
