from rest_framework import serializers

from companies.api.serializers import CurrentCompanyDefault
from companies.api.serializers.stock import MaterialSerializer
from companies.models import Point


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


class ConsumableMateriaSerializer(MaterialSerializer):
    stocks = serializers.ListField(child=serializers.JSONField())
    usage = serializers.ListField(child=serializers.JSONField())

    class Meta(MaterialSerializer.Meta):
        fields: tuple = MaterialSerializer.Meta.fields + ("stocks", "usage")
