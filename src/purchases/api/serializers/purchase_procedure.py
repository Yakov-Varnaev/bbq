from rest_framework import serializers

from companies.api.serializers import ProcedureSerializer
from purchases.api.serializers.purchase import PurchaseSerializer
from purchases.api.serializers.used_material import UsedMaterialWriteSerializer
from purchases.models import PurchaseProcedure


class PurchaseProcedureReadSerializer(serializers.ModelSerializer):
    procedure = ProcedureSerializer()
    purchase = PurchaseSerializer()

    class Meta:
        model = PurchaseProcedure
        _field = ("id", "procedure", "purchase")
        fields = _field
        only_read_fields = _field


class PurchaseProcedureWriteSerializer(serializers.ModelSerializer):
    materials = UsedMaterialWriteSerializer(many=True)

    class Meta:
        model = PurchaseProcedure
        _field = ("procedure", "purchase", "materials")
        fields = _field
        only_write_fields = _field

    def to_representation(self, instance: PurchaseProcedure) -> dict:
        return PurchaseProcedureReadSerializer(instance).data
