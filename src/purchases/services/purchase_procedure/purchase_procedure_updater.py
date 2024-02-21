from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from app.services import BaseService
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure, UsedMaterial
from purchases.types import UsedMaterialData


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

    def put_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[UsedMaterialData],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        used_materials.delete()
        used_material_objects = [UsedMaterial(procedure=purchase_procedure, **data) for data in used_materials_data]
        UsedMaterial.objects.bulk_create(used_material_objects)

    def patch_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[UsedMaterialData],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        materials = used_materials.values_list("material", flat=True)
        new_used_materials: list[UsedMaterial] = []
        for data in used_materials_data:
            material = data.pop("material")
            if material.id in materials:
                used_material = used_materials.get(material=material)
                used_material.amount = data["amount"]
                used_material.save()
            else:
                new_used_materials.append(
                    UsedMaterial(
                        procedure=purchase_procedure,
                        material=material,
                        amount=data["amount"],
                    )
                )
        UsedMaterial.objects.bulk_create(new_used_materials)

    def update_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[UsedMaterialData],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        if used_materials_data is not None:
            if self.serializer.partial:
                self.patch_used_materials(purchase_procedure, used_materials_data, used_materials)
            else:
                self.put_used_materials(purchase_procedure, used_materials_data, used_materials)

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[UsedMaterialData] = self.serializer.validated_data.pop("materials")
        purchase_procedure = get_object_or_404(PurchaseProcedure, id=self.purchase_procedure_id)
        used_materials: QuerySet[UsedMaterial] = purchase_procedure.used_materials.all()
        if self.serializer.validated_data is not None:
            for key, value in self.serializer.validated_data.items():
                setattr(purchase_procedure, key, value)
            purchase_procedure.save()
        if used_materials_data is not None:
            self.update_used_materials(purchase_procedure, used_materials_data, used_materials)
        return purchase_procedure
