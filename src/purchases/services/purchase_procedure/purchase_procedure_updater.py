from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from app.services import BaseService
from companies.models import StockMaterial
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure, UsedMaterial


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
        used_materials_data: list[dict[str, int]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        used_materials.delete()
        used_material_objects = [UsedMaterial(procedure=purchase_procedure, **data) for data in used_materials_data]
        UsedMaterial.objects.bulk_create(used_material_objects)

    def patch_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[dict[str, int | StockMaterial]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        new_materials: list[UsedMaterial] = []
        for data in used_materials_data:
            material = data.pop("material")
            if material in used_materials:
                material.amount = data["amount"]
                material.save()
            else:
                new_materials.append(
                    UsedMaterial(
                        procedure=purchase_procedure,
                        material=material,
                        amount=data["amount"],
                    )
                )
        UsedMaterial.objects.bulk_create(new_materials)

    def update_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[dict[str, int | StockMaterial]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        if used_materials_data is not None:
            if self.serializer.context["request"].method == "PUT":
                self.put_used_materials(purchase_procedure, used_materials_data, used_materials)
            if self.serializer.context["request"].method == "PATCH":
                self.patch_used_materials(purchase_procedure, used_materials_data, used_materials)

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[dict[str, StockMaterial | int]] = self.serializer.validated_data.pop("materials")
        purchase_procedure = get_object_or_404(PurchaseProcedure, id=self.purchase_procedure_id)
        used_materials: QuerySet[UsedMaterial] = purchase_procedure.used_materials.all()
        if self.serializer.validated_data is not None:
            for key, value in self.serializer.validated_data.items():
                setattr(purchase_procedure, key, value)
            purchase_procedure.save()
        if used_materials_data is not None:
            self.update_used_materials(purchase_procedure, used_materials_data, used_materials)
        return purchase_procedure
