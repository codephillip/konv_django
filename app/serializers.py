from rest_framework import serializers

from .models import (
    Announcement,
    Category,
    DeliverySpeed,
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
        fields = ['id', 'name', 'locations']


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
        fields = ['id', 'lat', 'lng', 'users', 'orders', 'district']


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'products']


class StockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Stock
        fields = ['id', 'units_in_stock', 'units_on_order', 'created_at', 'name', 'product']


class ShopSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )

    class Meta:
        model = Shop
        fields = ['id', 'name', 'is_special', 'products']


class ProductSerializer(serializers.ModelSerializer):
    stocks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Stock.objects.all(),
        required=False
    )
    orderitems = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=OrderItem.objects.all(),
        required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'expiry_date', 'weight', 'image', 'discount',
                  'description', 'color', 'price', 'stocks', 'orderitems', 'category', 'shop']


class PaymentSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    class Meta:
        model = Payment
        fields = ['id', 'created_at', 'paid_at', 'amount', 'status', 'customer', 'order']


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
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
    )
    deliveryspeed = serializers.PrimaryKeyRelatedField(
        queryset=DeliverySpeed.objects.all(),
    )

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'valid', 'delivery_method', 'expected_delivery_date_time',
                  'delivery_date_time', 'total_amount', 'payments', 'driver', 'location', 'deliveryspeed']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'units', 'valid', 'product']


class DeliverySpeedSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.all(),
        required=False
    )

    class Meta:
        model = DeliverySpeed
        fields = ['id', 'type', 'description', 'orders']


class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'body', 'image']