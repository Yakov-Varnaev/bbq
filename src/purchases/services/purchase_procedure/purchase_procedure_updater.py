from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction
from django.shortcuts import get_object_or_404

from app.services import BaseService
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure, UsedMaterial
from purchases.types import PurchaseProcedureData, UsedMaterialData


class PurchaseProcedureUpdater(BaseService):
    def __init__(
        self, serializer: BaseSerializer[PurchaseProcedureWriteSerializer], purchase_procedure_id: int
    ) -> None:
        self.serializer = serializer
        self.purchase_procedure_id = purchase_procedure_id

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def update_purchase_procedure(
        self, purchase_procedure: PurchaseProcedure, validated_data: PurchaseProcedureData
    ) -> None:
        for key, value in validated_data.items():
            setattr(purchase_procedure, key, value)
        purchase_procedure.save()

    def update_used_materials(
        self, purchase_procedure: PurchaseProcedure, used_materials_data: list[UsedMaterialData]
    ) -> None:
        purchase_procedure.used_materials.set(
            [
                UsedMaterial(
                    material=used_material_data["material"],
                    amount=used_material_data["amount"],
                    procedure=purchase_procedure,
                )
                for used_material_data in used_materials_data
            ]
        )

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[UsedMaterialData] = self.serializer.validated_data.pop("materials")
        purchase_procedure = get_object_or_404(PurchaseProcedure, id=self.purchase_procedure_id)
        if self.serializer.validated_data is not None:
            self.update_purchase_procedure(purchase_procedure, self.serializer.validated_data)
        if used_materials_data is not None:
            self.update_purchase_procedure(purchase_procedure, self.serializer.validated_data)
        return purchase_procedure
