# Generated by Django 5.1.3 on 2024-11-25 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roothub_cms_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'Trainer'), (3, 'Trainee')], default=1, max_length=10),
        ),
        migrations.DeleteModel(
            name='Prices',
        ),
    ]
