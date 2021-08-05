from django.conf.urls import include, re_path, url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from project import settings
from django.conf.urls.static import static

from .views import (
    AnnouncementViewSet,
    CategoryViewSet,
    DistrictViewSet,
    LocationViewSet,
    OrderItemViewSet,
    OrderViewSet,
    PaymentViewSet,
    ProductViewSet,
    ShopViewSet,
    StockViewSet,
    UserViewSet, OrderTrackerViewSet, BeyonicWebhook, ContactViewSet,
)


class OptionalSlashRouter(DefaultRouter):
    def __init__(self):
        super(DefaultRouter, self).__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()

router.register(r'users', UserViewSet, 'users')
router.register(r'districts', DistrictViewSet, 'districts')
router.register(r'locations', LocationViewSet, 'locations')
router.register(r'categories', CategoryViewSet, 'categories')
router.register(r'stock', StockViewSet, 'stock')
router.register(r'shops', ShopViewSet, 'shops')
router.register(r'contacts', ContactViewSet, 'contacts')
router.register(r'products', ProductViewSet, 'products')
router.register(r'payments', PaymentViewSet, 'payments')
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'orderitems', OrderItemViewSet, 'orderItems')
router.register(r'announcements', AnnouncementViewSet, 'announcements')
router.register(r'ordertrackers', OrderTrackerViewSet, 'ordertrackers')

schema_view = get_schema_view(
    openapi.Info(
        title="Konv",
        default_version='v1',
        description="API description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path('^', include(router.urls)),
    path(r'beyonic_webhook', csrf_exempt(BeyonicWebhook.as_view()), name='beyonic webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)