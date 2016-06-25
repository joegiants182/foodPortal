# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodPortalApp', '0003_auto_20150913_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='note',
            new_name='about',
        ),
    ]
