# Generated by Django 3.2.3 on 2021-06-17 22:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'announcement',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='DeliverySpeed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(blank=True, choices=[('ORDINARY', 'ORDINARY'), ('EXPRESS', 'EXPRESS')], max_length=8, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'deliverySpeed',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(50.0)])),
                ('lng', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(50.0)])),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='app.district')),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('status', models.CharField(blank=True, choices=[('PLACED', 'PLACED'), ('CANCELLED', 'CANCELLED'), ('REJECTED', 'REJECTED'), ('DELIVERED', 'DELIVERED')], default='placed', max_length=9, null=True)),
                ('valid', models.BooleanField(blank=True, default=True, null=True)),
                ('delivery_method', models.CharField(blank=True, choices=[('VEHICLE', 'VEHICLE'), ('MOTORCYCLE', 'MOTORCYCLE'), ('PICKUP', 'PICKUP')], default='motorcycle', max_length=10, null=True)),
                ('expected_delivery_date_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_date_time', models.DateTimeField(blank=True, null=True)),
                ('total_amount', models.IntegerField(blank=True, default=500, null=True, validators=[django.core.validators.MinValueValidator(500)])),
                ('deliveryspeed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app.deliveryspeed')),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('expiry_date', models.DateTimeField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, default=0.0, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('discount', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(blank=True, default=500, null=True, validators=[django.core.validators.MinValueValidator(500)])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.category')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('is_special', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'shop',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField(blank=True, null=True)),
                ('verified', models.BooleanField(blank=True, default=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('role', models.CharField(blank=True, choices=[('DEVELOPER', 'DEVELOPER'), ('CUSTOMER', 'CUSTOMER'), ('DRIVER', 'DRIVER'), ('ADMIN', 'ADMIN')], max_length=9, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='app.location')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('units_in_stock', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('units_on_order', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='app.product')),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.shop'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(500)])),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'PENDING'), ('CANCELLED', 'CANCELLED'), ('PAID', 'PAID'), ('EXPIRED', 'EXPIRED')], default='pending', max_length=9, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.user')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.order')),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('units', models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('valid', models.BooleanField(blank=True, default=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='app.product')),
            ],
            options={
                'db_table': 'orderItem',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='app.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='app.location'),
        ),
    ]
