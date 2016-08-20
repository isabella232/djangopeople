# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangopeople', '0002_load_fixtures'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='djangoperson',
            name='photo',
        ),
    ]
