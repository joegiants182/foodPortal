# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodPortalApp', '0004_auto_20151025_2247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='about',
            new_name='bio',
        ),
    ]
