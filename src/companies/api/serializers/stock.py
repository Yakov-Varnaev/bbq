from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from companies.api.serializers.defaults import CurrentPointDefault, CurrentStockDefault
from companies.models import Stock
from companies.models.stock import Material, StockMaterial


class MaterialSerializer(serializers.ModelSerializer):
    kind = serializers.CharField(source="kind.name")

    class Meta:
        model = Material
        fields = (
            "id",
            "brand",
            "name",
            "unit",
            "kind",
        )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            "id",
            "date",
            "status",
        )
        read_only_fields = (
            "id",
            "status",
        )


class StockCreateSerializer(serializers.ModelSerializer):
    point = serializers.HiddenField(default=CurrentPointDefault())

    class Meta:
        model = Stock
        fields = (
            "date",
            "point",
        )

    def to_representation(self, instance: Stock) -> dict:
        return StockSerializer(instance).data


class StockUpdateSerializer(StockCreateSerializer):
    class Meta:
        model = Stock
        fields = ("date", "point", "status")


class StockListSerializer(serializers.ModelSerializer):
    material_count = serializers.IntegerField()
    order_sum = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Stock
        fields = (
            "id",
            "date",
            "status",
            "material_count",
            "order_sum",
        )
        read_only_fields = (
            "id",
            "date",
            "status",
            "material_count",
            "order_sum",
        )


class StockMaterialSerializer(serializers.ModelSerializer):
    stock = serializers.HiddenField(default=CurrentStockDefault())

    class Meta:
        model = StockMaterial
        fields = ("id", "material", "quantity", "price", "stock")
        validators = [
            UniqueTogetherValidator(
                queryset=StockMaterial.objects.all(),
                fields=["stock", "material"],
            ),
        ]


class StockMaterialDetailedSerializer(StockMaterialSerializer):
    material = MaterialSerializer()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = StockMaterial
        fields = ("id", "material", "quantity", "price", "stock")
        read_only_fields = ("id", "material", "quantity", "price", "stock")
