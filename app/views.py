from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q

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
from .serializers import (
    AnnouncementSerializer,
    CategorySerializer,
    DistrictSerializer,
    LocationSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
    ShopSerializer,
    StockSerializer,
    UserSerializer,
    OrderTrackerSerializer, ContactSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filterset_fields = ['id', 'dob', 'verified', 'phone', 'role', 'payments', 'orders']


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'locations']


class LocationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.role == User.CUSTOMER:
            return Location.objects.filter(customer=user)
        else:
            return Location.objects.all()

    serializer_class = LocationSerializer
    permission_classes = []
    filterset_fields = ['id', 'lat', 'lng', 'customer', 'district', 'is_active']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'description', 'products']


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


class ContactViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.role == User.CUSTOMER:
            return Contact.objects.filter(customer=user)
        else:
            return Contact.objects.all()

    serializer_class = ContactSerializer
    permission_classes = []
    filterset_fields = ['id', 'customer', 'is_active', 'phone']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []
    filterset_fields = ['id', 'name', 'expiry_date', 'weight', 'discount',
                        'description', 'color', 'price', 'stocks', 'orderitems', 'category', 'shop']


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = []
    filterset_fields = ['id', 'created_at', 'paid_at', 'amount', 'status', 'customer', 'order']


class OrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        try:
            if user.role == User.CUSTOMER:
                return Order.objects.filter(Q(customer=user) | Q(is_curated_list=True))
            if user.role in [User.DEVELOPER, User.ADMIN]:
                return Order.objects.all()
            return Order.objects.filter(is_curated_list=True)
        except Exception as e:
            print(e)
            return Order.objects.filter(is_curated_list=True)

    serializer_class = OrderSerializer
    permission_classes = []
    filterset_fields = ['id', 'created_at', 'status', 'valid', 'delivery_method', 'expected_delivery_date_time',
                        'delivery_date_time', 'total_amount', 'payments', 'driver', 'location', 'delivery_speed']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = []
    filterset_fields = ['id', 'units', 'valid', 'product']


class OrderTrackerViewSet(viewsets.ModelViewSet):
    queryset = OrderTracker.objects.all()
    serializer_class = OrderTrackerSerializer
    permission_classes = []
    filterset_fields = ['name', 'order']


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = []
    filterset_fields = ['id', 'title', 'body']


class BeyonicWebhook(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            print('webhook reached')
            print(request.data)
            # todo update ordertracker status to 3(goods purchased)
            return Response('ACCEPT ' + request.data['remote_transaction_id'], status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
        return Response({"error": 400}, status=status.HTTP_400_BAD_REQUEST)
