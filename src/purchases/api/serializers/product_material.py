from rest_framework import serializers

from purchases.models import ProductMaterial


class ProductMaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = ["id", "price", "material"]


class ProductMaterialSerializer(ProductMaterialCreateSerializer):
    name = serializers.CharField()
    brand = serializers.CharField()
    kind = serializers.CharField()
    unit = serializers.CharField()

    class Meta(ProductMaterialCreateSerializer.Meta):
        model = ProductMaterial
        fields = ["id", "price", "name", "brand", "kind", "unit"]
