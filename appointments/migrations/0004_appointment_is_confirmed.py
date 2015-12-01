# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20151130_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
