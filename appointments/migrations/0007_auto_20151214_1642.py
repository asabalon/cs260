# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('appointments', '0006_appointment_is_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(null=True, blank=True, max_length=25)),
            ],
            options={
                'db_table': 'appointment_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(null=True, blank=True, max_length=50)),
            ],
            options={
                'db_table': 'role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user_details', models.ForeignKey(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female')], null=True, blank=True, max_length=1)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('phone_number', models.CharField(null=True, blank=True, max_length=10)),
                ('mobile_number', models.CharField(null=True, blank=True, max_length=15)),
                ('address', models.CharField(null=True, blank=True, max_length=50)),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'User Details',
                'db_table': 'user_details',
                'managed': False,
                'verbose_name_plural': 'User Details',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'db_table': 'user_role',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user_ptr',
        ),
        migrations.RemoveField(
            model_name='pet',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='veterinaryphysician',
            name='user_ptr',
        ),
        migrations.AlterModelOptions(
            name='appointment',
            options={'managed': False},
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor', models.ForeignKey(primary_key=True, serialize=False, to='appointments.UserDetails')),
                ('specialization', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'doctor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient', models.ForeignKey(primary_key=True, serialize=False, to='appointments.UserDetails')),
                ('patient_since', models.DateField()),
                ('followup_date', models.DateField(null=True, blank=True)),
                ('referred_by', models.CharField(null=True, blank=True, max_length=20)),
            ],
            options={
                'db_table': 'patient',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Pet',
        ),
        migrations.DeleteModel(
            name='VeterinaryPhysician',
        ),
    ]
