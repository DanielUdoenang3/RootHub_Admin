# Generated by Django 5.1.3 on 2024-11-29 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roothub_cms_app', '0005_admin_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='blank.webp', upload_to='profile_pic'),
        ),
    ]
