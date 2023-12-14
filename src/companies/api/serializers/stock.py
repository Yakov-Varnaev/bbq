from rest_framework import serializers

from companies.api.serializers.defaults import CurrentPointDefault
from companies.models import Stock


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
