from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin, ModelAdminGroup
from wagtail.core import hooks

from app.models import *


class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = "Products"
    menu_icon = "doc-full"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("id", "name", "expiry_date", "weight", "image", "discount",
                    "description", "color", "price", "category", "shop", "created_at")
    list_filter = ("category", "shop")
    search_fields = ("name",)


class ShopAdmin(ModelAdmin):
    model = Shop
    menu_label = "Shop"
    menu_icon = "media"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "image")
    search_fields = ("name",)


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = "Category"
    menu_icon = "media"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "image")
    search_fields = ("name",)


class LocationAdmin(ModelAdmin):
    model = Location
    menu_label = "Locations"
    menu_icon = "form"
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("lat", "lng")


class OrderAdmin(ModelAdmin):
    model = Order
    menu_label = "Order"
    menu_icon = "media"
    menu_order = 500
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("valid", "customer", "created_at")
    search_fields = ("customer",)


class OrderItemAdmin(ModelAdmin):
    model = OrderItem
    menu_label = "OrderItem"
    menu_icon = "media"
    menu_order = 600
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("valid", "order", "created_at")
    search_fields = ("order",)


modeladmin_register(ProductAdmin)
modeladmin_register(ShopAdmin)
modeladmin_register(LocationAdmin)
modeladmin_register(CategoryAdmin)
modeladmin_register(OrderAdmin)
modeladmin_register(OrderItemAdmin)


@hooks.register("construct_main_menu")
def hide_default_explorer_menu(request, menu_items):
    menu_items[:] = [item for item in menu_items if
                     item.name not in ["settings", "images", "documents", "reports", "explorer"]]
