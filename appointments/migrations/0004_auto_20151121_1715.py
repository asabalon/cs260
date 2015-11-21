# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_veterinaryphysician'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='veterinary_physician',
            field=models.ForeignKey(to='appointments.VeterinaryPhysician'),
        ),
    ]
