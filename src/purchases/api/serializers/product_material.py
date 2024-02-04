from rest_framework import serializers

from purchases.models import ProductMaterial


class ProductMaterialSerializer(serializers.ModelSerializer):
    brand = serializers.CharField()
    name = serializers.CharField()
    kind = serializers.CharField()
    unit = serializers.CharField()

    class Meta:
        model = ProductMaterial
        fields = ("id", "price", "brand", "name", "kind", "unit")


class ProductMaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        exclude = ("archived", "created", "modified")
