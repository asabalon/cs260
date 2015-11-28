# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('pet_description', models.CharField(blank=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\s,.?!-]*$', 'No Special Characters are allowed in this field')], max_length=500)),
                ('visit_schedule', models.DateTimeField()),
                ('visit_description', models.CharField(validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\s,.?!-]*$', 'No Special Characters are allowed in this field')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('breed', models.CharField(max_length=50)),
                ('age_in_months', models.PositiveSmallIntegerField(default=0)),
                ('owner', models.ForeignKey(to='appointments.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='VeterinaryPhysician',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='pet_name',
            field=models.ForeignKey(to='appointments.Pet'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='pet_owner',
            field=models.ForeignKey(to='appointments.Customer'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='veterinary_physician',
            field=models.ForeignKey(to='appointments.VeterinaryPhysician'),
        ),
    ]
