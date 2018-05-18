# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CSS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50, blank=True)),
                ('titulo', models.CharField(max_length=50, blank=True)),
                ('color', models.CharField(max_length=50, blank=True)),
                ('size', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('enlace', models.TextField()),
                ('direccion', models.CharField(max_length=200)),
                ('barrio', models.CharField(max_length=50)),
                ('distrito', models.CharField(max_length=50)),
                ('contacto', models.CharField(max_length=150)),
                ('accesibilidad', models.CharField(max_length=2)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Seleccionado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now=True)),
                ('museo_id', models.ForeignKey(to='museos.Museo')),
                ('user', models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo_id',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
