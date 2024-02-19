from rest_framework import serializers

from purchases.models import UsedMaterial


class UsedMaterialReadSerializer(serializers.ModelSerializer):
    brand = serializers.CharField()
    name = serializers.CharField()
    kind = serializers.CharField()
    unit = serializers.CharField()
    amount = serializers.IntegerField()

    class Meta:
        model = UsedMaterial
        _fields = ("id", "procedure", "brand", "name", "kind", "unit", "amount")
        fields = _fields
        only_read_fields = _fields


class UserMaterialWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedMaterial
        _fields = ("material", "amount")
        fields = _fields
        only_write_fields = _fields
