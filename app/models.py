import random
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from app.utilities.constants import phone_regex


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

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    dob = models.DateField(null=True, blank=True)
    verified = models.BooleanField(null=True, blank=True, default=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex=phone_regex,
            message='Phone number is invalid',
        )
    ])
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=ADMIN)
    profile_pic = models.ImageField(upload_to='thumbnail/profile/', null=True, blank=True)
    # allows user to access these fields in /auth/me
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["role", "email"]

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


class Contact(BaseAbstractModel):
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True, validators=[
        RegexValidator(
            regex=phone_regex,
            message='Phone number is invalid',
        )
    ])
    is_active = models.BooleanField(default=False)
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contacts')


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
    name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    district = models.ForeignKey('District', on_delete=models.SET_NULL,
                                 related_name='locations', null=True, blank=True)
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='locations', null=True, blank=True)

    class Meta:
        db_table = "location"

    def __str__(self):
        return self.name


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
    KG = 'kg'
    LITRE = 'litre'
    PIECE = 'piece'
    BUNCH = 'bunch'
    METRIC_CHOICES = [
        (KG, KG),
        (LITRE, LITRE),
        (PIECE, PIECE),
        (BUNCH, BUNCH)
    ]
    name = models.CharField(max_length=255, unique=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    weight = models.FloatField(validators=[MinValueValidator(0.0)],
                               null=True, blank=True, default=0.0)
    image = models.ImageField(upload_to='thumbnail/product/', null=True, blank=True)
    metric = models.CharField(max_length=30, choices=METRIC_CHOICES, default=KG)
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
    PENDING = 'pending'
    CANCELLED = 'cancelled'
    PAID = 'paid'
    EXPIRED = 'expired'
    STATUS_CHOICES = [
        (PENDING, 'pending'),
        (CANCELLED, 'cancelled'),
        (PAID, 'paid'),
        (EXPIRED, 'expired')
    ]

    CASH = 'cash'
    MOMO = 'mobile money'
    CARD = 'card'
    PAYMENT_CHOICES = [
        (CASH, 'cash'),
        (MOMO, 'mobile money'),
        (CARD, 'card')
    ]

    paid_at = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField(validators=[MinValueValidator(500)])
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              null=True, blank=True, default=PENDING)
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='payments')
    momo_phone_number = models.CharField(max_length=20, null=True, blank=True)
    card_number = models.CharField(max_length=200, null=True, blank=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES,
                                      null=True, blank=True, default=CASH)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')

    class Meta:
        db_table = "payment"

    def __str__(self):
        return self.customer.username + " " + str(self.status)


def generate_random_token():
    return str(random.randint(10000000, 99999999))


class Order(BaseAbstractModel):
    PLACED = 'placed'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'
    DELIVERED = 'delivered'
    STATUS_CHOICES = [
        (PLACED, 'placed'),
        (CANCELLED, 'cancelled'),
        (REJECTED, 'rejected'),
        (DELIVERED, 'delivered')
    ]
    VEHICLE = 'vehicle'
    MOTORCYCLE = 'motorcycle'
    PICKUP = 'pickup'
    DELIVERY_METHOD_CHOICES = [
        (VEHICLE, 'vehicle'),
        (MOTORCYCLE, 'motorcycle'),
        (PICKUP, 'pickup')
    ]
    ORDINARY = 'ordinary'
    EXPRESS = 'express'
    TYPE_CHOICES = [
        (ORDINARY, 'ordinary'),
        (EXPRESS, 'express')
    ]

    delivery_speed = models.CharField(max_length=30, choices=TYPE_CHOICES, default=ORDINARY)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              null=True, blank=True, default='placed')
    valid = models.BooleanField(null=True, blank=True, default=True)
    delivery_method = models.CharField(
        max_length=10, choices=DELIVERY_METHOD_CHOICES, null=True, blank=True, default='motorcycle')
    # todo calculate this from location field and delivery_method
    expected_delivery_date_time = models.DateTimeField(null=True, blank=True)
    delivery_date_time = models.DateTimeField(null=True, blank=True)
    total_amount = models.IntegerField(
        validators=[MinValueValidator(500)], null=True, blank=True, default=500)
    # todo calculate this from orderitems
    sub_total_amount = models.IntegerField(
        validators=[MinValueValidator(500)], null=True, blank=True, default=500)
    order_tracking_number = models.CharField(default=generate_random_token, max_length=30, null=True, blank=True)
    delivery_fee = models.IntegerField(
        validators=[MinValueValidator(500)], null=True, blank=True, default=5000)
    driver = models.ForeignKey('User', on_delete=models.SET_NULL,
                               related_name='orders', null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_curated_list = models.BooleanField(null=True, blank=True, default=False)
    image = models.ImageField(upload_to='thumbnail/curated/', null=True, blank=True)
    customer = models.ForeignKey('User', on_delete=models.SET_NULL,
                                 related_name='customer_orders', null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    class Meta:
        db_table = "order"
        ordering = ('-created_at',)

    def __str__(self):
        return self.order_tracking_number


class OrderItem(BaseAbstractModel):
    units = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True, default=1)
    valid = models.BooleanField(null=True, blank=True, default=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orderitems')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='orderitems', null=True, blank=True)

    class Meta:
        db_table = "orderItem"

    def __str__(self):
        return self.product.name + " " + str(self.id)


class Announcement(BaseAbstractModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='thumbnail/announcement/', null=True, blank=True)

    class Meta:
        db_table = "announcement"

    def __str__(self):
        return self.title


class OrderTracker(BaseAbstractModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='ordertrackers', null=True, blank=True)

    class Meta:
        unique_together = ('number', 'order')
        ordering = ('number',)

    def __str__(self):
        return self.order.order_tracking_number + " " + str(self.id)


def save_initial_customer_contact(sender, instance, created, update_fields, **kwargs):
    if created and instance.role == User.CUSTOMER:
        Contact(phone=instance.phone, customer=instance, is_active=True).save()


def deactivate_mm_numbers(sender, instance, created, update_fields, **kwargs):
    Contact.objects.filter(customer=instance.customer).update(is_active=False)
    Contact.objects.filter(id=instance.id).update(is_active=True)


def deactivate_locations(sender, instance, created, update_fields, **kwargs):
    Location.objects.filter(customer=instance.customer).update(is_active=False)
    Location.objects.filter(id=instance.id).update(is_active=True)


post_save.connect(save_initial_customer_contact, sender=User)
post_save.connect(deactivate_mm_numbers, sender=Contact)
post_save.connect(deactivate_locations, sender=Location)
