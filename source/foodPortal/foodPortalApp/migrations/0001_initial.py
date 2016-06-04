# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('cost', models.CharField(max_length=7, default='0.00')),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False, auto_created=True, primary_key=True)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('room', models.CharField(max_length=4)),
                ('note', models.TextField(max_length=1024, default="None :'(")),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('restaurant', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.URLField(blank=True)),
                ('curator', models.ForeignKey(to='foodPortalApp.Member', related_name='curator', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='MenuSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('menu', models.ForeignKey(to='foodPortalApp.Menu', related_name='menu')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000, default='')),
                ('menu', models.ForeignKey(to='foodPortalApp.Menu', related_name='optionMenu', default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(max_digits=6, decimal_places=2)),
                ('status', models.CharField(default='Open', max_length=256, choices=[('Open', 'Open'), ('Placed', 'Placed'), ('Paid For', 'Paid For'), ('On The Way', 'On The Way'), ('In The Kitchen', 'In The Kitchen'), ('Closed', 'Closed')])),
                ('dateCreated', models.DateField(auto_now_add=True)),
                ('timeCreated', models.TimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(to='foodPortalApp.Member', related_name='customer', default=1)),
                ('items', models.ManyToManyField(to='foodPortalApp.Option')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='menu',
            field=models.ForeignKey(to='foodPortalApp.Menu', related_name='itemMenu', default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='option',
            field=models.ManyToManyField(to='foodPortalApp.Option', related_name='options'),
        ),
        migrations.AddField(
            model_name='item',
            name='section',
            field=models.ForeignKey(to='foodPortalApp.MenuSection', related_name='section', default=1),
        ),
    ]
