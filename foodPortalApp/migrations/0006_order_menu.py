# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodPortalApp', '0005_auto_20151025_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='menu',
            field=models.ForeignKey(to='foodPortalApp.Menu', default=1),
        ),
    ]
