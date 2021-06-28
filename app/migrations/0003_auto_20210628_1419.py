# Generated by Django 3.2.3 on 2021-06-28 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210628_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryspeed',
            name='type',
            field=models.CharField(blank=True, choices=[('ORDINARY', 'ORDINARY'), ('EXPRESS', 'EXPRESS')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('PLACED', 'PLACED'), ('CANCELLED', 'CANCELLED'), ('REJECTED', 'REJECTED'), ('DELIVERED', 'DELIVERED')], default='placed', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('CANCELLED', 'CANCELLED'), ('PAID', 'PAID'), ('EXPIRED', 'EXPIRED')], default='pending', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('developer', 'developer'), ('customer', 'customer'), ('driver', 'driver'), ('admin', 'admin')], default='customer', max_length=30),
        ),
    ]
