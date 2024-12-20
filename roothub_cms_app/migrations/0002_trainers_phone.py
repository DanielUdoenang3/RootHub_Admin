# Generated by Django 5.1.3 on 2024-11-28 06:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roothub_cms_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainers',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
