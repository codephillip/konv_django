from rest_framework import viewsets

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
from .serializers import (
    AnnouncementSerializer,
    CategorySerializer,
    DeliverySpeedSerializer,
    DistrictSerializer,
    LocationSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
    ShopSerializer,
    StockSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filterset_fields = ['id', 'dob', 'verified', 'phone', 'role', 'payments', 'orders', 'location']


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'locations']


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = []
    filterset_fields = ['id', 'lat', 'lng', 'users', 'orders', 'district']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'description', 'image', 'products']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = []
    filterset_fields = ['id', 'units_in_stock', 'units_on_order', 'created_at', 'name', 'product']


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'is_special', 'products']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'expiry_date', 'weight', 'image', 'discount',
                        'description', 'color', 'price', 'stocks', 'orderitems', 'category', 'shop']


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = []
    filterset_fields = ['id', 'created_at', 'paid_at', 'amount', 'status', 'customer', 'order']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = []
    filterset_fields = ['id', 'created_at', 'status', 'valid', 'delivery_method', 'expected_delivery_date_time',
                        'delivery_date_time', 'total_amount', 'payments', 'driver', 'location', 'deliveryspeed']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = []
    filterset_fields = ['id', 'units', 'valid', 'product']


class DeliverySpeedViewSet(viewsets.ModelViewSet):
    queryset = DeliverySpeed.objects.all()
    serializer_class = DeliverySpeedSerializer
    permission_classes = []
    filterset_fields = ['id', 'type', 'description', 'orders']


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = []
    filterset_fields = ['id', 'title', 'body', 'image']
