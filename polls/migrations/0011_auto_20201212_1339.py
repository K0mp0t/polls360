# Generated by Django 3.1.2 on 2020-12-12 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20201212_1324'),
        ('polls', '0010_auto_20201212_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.team'),
        ),
    ]
