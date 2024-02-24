from rest_framework import serializers

from purchases.models import UsedMaterial


class UsedMaterialReadSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="material.material.brand")
    name = serializers.CharField(source="material.material.name")
    kind = serializers.CharField(source="material.material.kind")
    unit = serializers.CharField(source="material.material.unit")

    class Meta:
        model = UsedMaterial
        _fields = ("id", "procedure", "brand", "name", "kind", "unit", "amount")
        fields = _fields
        read_only_fields = _fields


class UsedMaterialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedMaterial
        _fields = ("material", "amount")
        fields = _fields
        write_only_fields = _fields
