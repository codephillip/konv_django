from rest_framework import serializers

from .models import (
    Announcement,
    Category,
    District,
    Location,
    Order,
    OrderItem,
    Payment,
    Product,
    Shop,
    Stock,
    User,
)


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Payment.objects.all(),
        required=False
    )
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.all(),
        required=False
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['id', 'dob', 'verified', 'phone', 'role', 'payments', 'orders', 'location']


class DistrictSerializer(serializers.ModelSerializer):
    locations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = District
        fields = ['id', 'name', 'locations', 'created_at']


class LocationSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.all(),
        required=False
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        required=False
    )

    class Meta:
        model = Location
        fields = ['id', 'lat', 'lng', 'users', 'orders', 'district', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'products', 'created_at']


class StockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Stock
        fields = ['id', 'units_in_stock', 'units_on_order', 'created_at', 'name', 'product', 'created_at']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'image', 'is_special', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'expiry_date', 'weight', 'image', 'discount',
                  'description', 'color', 'price', 'category', 'shop', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    class Meta:
        model = Payment
        fields = ['id', 'created_at', 'paid_at', 'amount', 'status', 'customer', 'order', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    payments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Payment.objects.all(),
        required=False
    )
    driver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )
    orderitems = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=OrderItem.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'valid', 'delivery_method', 'expected_delivery_date_time',
                  'delivery_date_time', 'total_amount', 'payments', 'driver', 'location', 'delivery_speed',
                  'orderitems', 'customer', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'units', 'valid', 'product', 'order', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'body', 'image', 'created_at']
