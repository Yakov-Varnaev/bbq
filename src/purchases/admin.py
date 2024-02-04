from django.contrib import admin

from app.admin import ModelAdmin
from purchases.models import ProductMaterial


@admin.register(ProductMaterial)
class ProductMaterialAdmin(ModelAdmin):
    list_display = (
        "material",
        "price",
        "archived",
        "created",
        "modified",
    )
    search_fields = (
        "material__material__name",
        "material__material__brand",
        "material__material__kind",
    )
