# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0002_auto_20151130_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='veterinaryphysician',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='veterinaryphysician',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='veterinaryphysician',
            name='email_address',
        ),
        migrations.RemoveField(
            model_name='veterinaryphysician',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='veterinaryphysician',
            name='id',
        ),
        migrations.RemoveField(
            model_name='veterinaryphysician',
            name='last_name',
        ),
        migrations.AddField(
            model_name='veterinaryphysician',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, default='', primary_key=True, auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False),
            preserve_default=False,
        ),
    ]
