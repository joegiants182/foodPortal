# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodPortalApp', '0002_auto_20150913_0109'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('cost', models.DecimalField(max_digits=6, decimal_places=2)),
                ('item', models.ForeignKey(to='foodPortalApp.Item')),
                ('option', models.ForeignKey(to='foodPortalApp.Option')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='options',
        ),
        migrations.AddField(
            model_name='order',
            name='orderItems',
            field=models.ManyToManyField(to='foodPortalApp.OrderItem'),
        ),
    ]
