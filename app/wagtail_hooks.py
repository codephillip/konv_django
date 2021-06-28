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
    list_display = ("name", "image", "created_at")
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
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "image")
    search_fields = ("name",)


class LocationAdmin(ModelAdmin):
    model = Location
    menu_label = "Locations"
    menu_icon = "form"
    menu_order = 100
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("lat", "lng")
    # list_filter = ("article", "category")
    # search_fields = ("content",)


modeladmin_register(ProductAdmin)
modeladmin_register(ShopAdmin)
modeladmin_register(LocationAdmin)
modeladmin_register(CategoryAdmin)



@hooks.register('construct_main_menu')
def hide_default_explorer_menu(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in ['settings', 'images', 'documents', 'reports', 'explorer']]