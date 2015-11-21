# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='visitSchedule',
            new_name='visit_schedule',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='petDescription',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='petOwnerName',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='veterinaryPhysician',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='visitDescription',
        ),
        migrations.AddField(
            model_name='appointment',
            name='pet_description',
            field=models.CharField(default=datetime.datetime(2015, 11, 11, 6, 54, 40, 981974, tzinfo=utc), max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='veterinary_physician',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='visit_description',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='pet_owner',
            field=models.ForeignKey(default='', to='appointments.Customer'),
            preserve_default=False,
        ),
    ]
