from rest_framework import serializers

from companies.api.serializers.defaults import CurrentCompanyDefault
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
