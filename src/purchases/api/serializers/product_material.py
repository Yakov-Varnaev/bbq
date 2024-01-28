from rest_framework import serializers

from purchases.models import ProductMaterial


class ProductMaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = ("id", "price", "material")


class ProductMaterialSerializer(ProductMaterialCreateSerializer):
    class Meta(ProductMaterialCreateSerializer.Meta):
        model = ProductMaterial
        fields = ("id", "price", "name", "brand", "type", "unit")
