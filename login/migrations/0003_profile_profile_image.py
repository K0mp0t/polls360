# Generated by Django 3.1.2 on 2020-12-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20201212_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
