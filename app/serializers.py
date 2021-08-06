from rest_framework import serializers
from djoser.serializers import TokenSerializer
from rest_framework.authtoken.models import Token

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
    OrderTracker, Contact,
)


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['dob', 'verified', 'phone', 'role', 'email', 'first_name', 'last_name', 'username', 'password']

    def create(self, validated_data):
        """
        Sets user password.
        NOTE: Without this, User will never sign_in and password will not be encrypted
        """
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


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

    class Meta:
        model = User
        fields = ['id', 'dob', 'verified', 'first_name', 'last_name', 'phone', 'role', 'payments', 'orders']
        # required to resolve swagger schema conflict
        ref_name = "UserModel"


class CustomTokenSerializer(TokenSerializer):
    """
    Override the djoser(https://djoser.readthedocs.io/en/latest/) token serializer
    Allows us to return user details along side the djoser token
    """
    auth_token = serializers.CharField(source='key')
    user = UserSerializer()

    class Meta:
        model = Token
        fields = (
            'auth_token', 'user'
        )


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
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(),
        required=False
    )

    class Meta:
        model = Location
        fields = ['id', 'lat', 'lng', 'name', 'district', 'created_at']


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone', 'is_active', 'customer', 'created_at']


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
        fields = ['id', 'created_at', 'paid_at', 'amount', 'status', 'customer', 'order', 'momo_phone_number',
                  'card_number', 'payment_method', 'created_at']


class LastOrderTrackerStatusSerializer(serializers.Field):
    def to_representation(self, order):
        try:
            return OrderTracker.objects.filter(order=order).last().name
        except AttributeError as e:
            print(e)
            return "Order Placed"


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
    last_tracker_status = LastOrderTrackerStatusSerializer(source='*', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'valid', 'delivery_method', 'expected_delivery_date_time',
                  'delivery_date_time', 'total_amount', 'payments', 'driver', 'location', 'delivery_speed',
                  'orderitems', 'customer', 'delivery_fee', 'sub_total_amount', 'order_tracking_number',
                  'last_tracker_status', 'created_at']


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


class OrderTrackerSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
    )

    class Meta:
        model = OrderTracker
        fields = ['id', 'order', 'name', 'number', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'body', 'image', 'created_at']
