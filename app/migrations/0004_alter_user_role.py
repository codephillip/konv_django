# Generated by Django 3.2.3 on 2021-06-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210628_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('developer', 'developer'), ('customer', 'customer'), ('driver', 'driver'), ('admin', 'admin')], default='admin', max_length=30),
        ),
    ]
