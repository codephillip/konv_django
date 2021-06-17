from django.contrib import admin

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

admin.site.register(User)
admin.site.register(District)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliverySpeed)
admin.site.register(Announcement)
