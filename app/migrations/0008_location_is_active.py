# Generated by Django 3.2.3 on 2021-08-06 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]