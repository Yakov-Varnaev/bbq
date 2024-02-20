from rest_framework import serializers

from purchases.models import UsedMaterial


class UsedMaterialReadSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="material.material.brand")
    name = serializers.CharField(source="material.material.name")
    kind = serializers.CharField(source="material.material.kind")
    unit = serializers.CharField(source="material.material.unit")
    amount = serializers.IntegerField()

    class Meta:
        model = UsedMaterial
        _fields = ("id", "procedure", "brand", "name", "kind", "unit", "amount")
        fields = _fields
        only_read_fields = _fields


class UsedMaterialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedMaterial
        _fields = ("material", "amount")
        fields = _fields
        only_write_fields = _fields
