# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_auto_20151121_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='veterinaryphysician',
            name='email_address',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='pet_description',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\s,.?!-]*$', 'No Special Characters are allowed in this field')], max_length=500),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='visit_description',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\s,.?!-]*$', 'No Special Characters are allowed in this field')], max_length=500),
        ),
    ]
