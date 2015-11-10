# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('petOwnerName', models.CharField(editable=False, max_length=50)),
                ('petDescription', models.CharField(max_length=100)),
                ('visitSchedule', models.DateTimeField()),
                ('visitDescription', models.CharField(max_length=100)),
                ('veterinaryPhysician', models.CharField(max_length=100)),
            ],
        ),
    ]
