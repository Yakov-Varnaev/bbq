from rest_framework import serializers

from companies.api.serializers import CurrentCompanyDefault
from companies.models import Point, StockMaterial


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Point


class PointCreateSerializer(PointSerializer):
    company = serializers.HiddenField(default=CurrentCompanyDefault())

    def to_representation(self, instance: Point) -> dict:
        return PointSerializer(instance).data

    class Meta(PointSerializer.Meta):
        pass


class ConsumableMateriaSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="material.id")  # noqa: VNE003
    brand = serializers.CharField(source="material.brand")
    name = serializers.CharField(source="material.name")
    unit = serializers.CharField(source="material.unit")
    kind = serializers.CharField(source="material.kind.name")
    stocks = serializers.ListField(child=serializers.JSONField())
    usage = serializers.ListField(child=serializers.JSONField())

    class Meta:
        model = StockMaterial
        fields = (
            "id",
            "brand",
            "name",
            "unit",
            "kind",
            "stocks",
            "usage",
        )
