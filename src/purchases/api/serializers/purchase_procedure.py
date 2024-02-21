from rest_framework import serializers

from companies.api.serializers import ProcedureSerializer
from purchases.api.serializers.purchase import PurchaseSerializer
from purchases.api.serializers.used_material import UsedMaterialReadSerializer, UsedMaterialWriteSerializer
from purchases.models import PurchaseProcedure


class PurchaseProcedureReadSerializer(serializers.ModelSerializer):
    procedure = ProcedureSerializer()
    purchase = PurchaseSerializer()
    materials = UsedMaterialReadSerializer(source="used_materials", many=True)

    class Meta:
        model = PurchaseProcedure
        _fields = ("id", "procedure", "purchase", "materials")
        fields = _fields
        read_only_fields = _fields


class PurchaseProcedureWriteSerializer(serializers.ModelSerializer):
    materials = UsedMaterialWriteSerializer(many=True)

    class Meta:
        model = PurchaseProcedure
        _fields = ("procedure", "purchase", "materials")
        fields = _fields
        write_only_fields = _fields

    def to_representation(self, instance: PurchaseProcedure) -> dict:
        return PurchaseProcedureReadSerializer(instance).data

    def validate_materials(self, materials: list[dict[str, int]]) -> list[dict[str, int]]:
        material_ids = [material["material"] for material in materials]
        if len(material_ids) != len(set(material_ids)):
            raise serializers.ValidationError("Materials must be unique.")
        return materials
