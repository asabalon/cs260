# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_remove_appointment_is_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
