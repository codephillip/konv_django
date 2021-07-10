import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    DEVELOPER = 'developer'
    CUSTOMER = 'customer'
    DRIVER = 'driver'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (DEVELOPER, 'developer'),
        (CUSTOMER, 'customer'),
        (DRIVER, 'driver'),
        (ADMIN, 'admin')
    ]

    dob = models.DateField(null=True, blank=True)
    verified = models.BooleanField(null=True, blank=True, default=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ADMIN)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL,
                                 related_name='users', null=True, blank=True)
    profile_pic = models.ImageField(upload_to='thumbnail/profile/', null=True, blank=True)
    # allows user to access these fields in /auth/me
    REQUIRED_FIELDS = ["phone", "role", "email"]

    def __str__(self):
        return self.username


class BaseAbstractModel(models.Model):
    """
     This model defines base models that implements common fields like:
     created_at
     updated_at
     is_deleted
    """
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        """soft  delete a model instance"""
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
        ordering = ['-created_at']


class District(BaseAbstractModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "district"

    def __str__(self):
        return self.name


class Location(BaseAbstractModel):
    lat = models.FloatField(validators=[MinValueValidator(
        0.0), MaxValueValidator(50.0)], null=True, blank=True)
    lng = models.FloatField(validators=[MinValueValidator(
        0.0), MaxValueValidator(50.0)], null=True, blank=True)
    district = models.ForeignKey('District', on_delete=models.SET_NULL,
                                 related_name='locations', null=True, blank=True)

    class Meta:
        db_table = "location"


class Category(BaseAbstractModel):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='thumbnail/category/', null=True, blank=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Stock(BaseAbstractModel):
    units_in_stock = models.IntegerField(
        validators=[MinValueValidator(0)], null=True, blank=True, default=0)
    units_on_order = models.IntegerField(
        validators=[MinValueValidator(0)], null=True, blank=True, default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stocks')

    class Meta:
        db_table = "stock"

    def __str__(self):
        return self.name


class Shop(BaseAbstractModel):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    is_special = models.BooleanField(null=True, blank=True, default=False)
    image = models.ImageField(upload_to='thumbnail/shop/', null=True, blank=True)

    class Meta:
        db_table = "shop"

    def __str__(self):
        return self.name


class Product(BaseAbstractModel):
    name = models.CharField(max_length=255, unique=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    weight = models.FloatField(validators=[MinValueValidator(0.0)],
                               null=True, blank=True, default=0.0)
    image = models.ImageField(upload_to='thumbnail/product/', null=True, blank=True)
    discount = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(99)], null=True, blank=True, default=0)
    description = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(
        validators=[MinValueValidator(500)], null=True, blank=True, default=500)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class Payment(BaseAbstractModel):
    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'
    PAID = 'PAID'
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (CANCELLED, 'CANCELLED'),
        (PAID, 'PAID'),
        (EXPIRED, 'EXPIRED')
    ]

    paid_at = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField(validators=[MinValueValidator(500)])
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              null=True, blank=True, default='pending')
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')

    class Meta:
        db_table = "payment"

    def __str__(self):
        return self.customer.id


class Order(BaseAbstractModel):
    PLACED = 'PLACED'
    CANCELLED = 'CANCELLED'
    REJECTED = 'REJECTED'
    DELIVERED = 'DELIVERED'
    STATUS_CHOICES = [
        (PLACED, 'PLACED'),
        (CANCELLED, 'CANCELLED'),
        (REJECTED, 'REJECTED'),
        (DELIVERED, 'DELIVERED')
    ]
    VEHICLE = 'VEHICLE'
    MOTORCYCLE = 'MOTORCYCLE'
    PICKUP = 'PICKUP'
    DELIVERY_METHOD_CHOICES = [
        (VEHICLE, 'VEHICLE'),
        (MOTORCYCLE, 'MOTORCYCLE'),
        (PICKUP, 'PICKUP')
    ]

    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              null=True, blank=True, default='placed')
    valid = models.BooleanField(null=True, blank=True, default=True)
    delivery_method = models.CharField(
        max_length=10, choices=DELIVERY_METHOD_CHOICES, null=True, blank=True, default='motorcycle')
    expected_delivery_date_time = models.DateTimeField(null=True, blank=True)
    delivery_date_time = models.DateTimeField(null=True, blank=True)
    total_amount = models.IntegerField(
        validators=[MinValueValidator(500)], null=True, blank=True, default=500)
    driver = models.ForeignKey('User', on_delete=models.SET_NULL,
                               related_name='orders', null=True, blank=True)
    customer = models.ForeignKey('User', on_delete=models.SET_NULL,
                                 related_name='customer_orders', null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='orders')
    deliveryspeed = models.ForeignKey(
        'DeliverySpeed', on_delete=models.CASCADE, related_name='orders')

    class Meta:
        db_table = "order"


class OrderItem(BaseAbstractModel):
    units = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True, default=1)
    valid = models.BooleanField(null=True, blank=True, default=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orderitems')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderitems', null=True, blank=True)

    class Meta:
        db_table = "orderItem"


class DeliverySpeed(BaseAbstractModel):
    ORDINARY = 'ORDINARY'
    EXPRESS = 'EXPRESS'
    TYPE_CHOICES = [
        (ORDINARY, 'ORDINARY'),
        (EXPRESS, 'EXPRESS')
    ]

    type = models.CharField(max_length=30, choices=TYPE_CHOICES, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "deliverySpeed"


class Announcement(BaseAbstractModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='thumbnail/announcement/', null=True, blank=True)

    class Meta:
        db_table = "announcement"
