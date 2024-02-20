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
        used_materials_data: list[dict[str, int]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        used_materials_id = used_materials.values_list("material__id", flat=True)
        create_used_materials: list[int] = []
        update_used_materials: list[int] = []
        for data in used_materials_data:
            _id = data["material"]
            update_used_materials.append(_id) if _id in used_materials_id else create_used_materials.append(_id)
        new_used_material: list[UsedMaterial] = []
        stock_materials = StockMaterial.objects.filter(id__in=create_used_materials)
        for data in used_materials_data:
            _id = data.pop("material")
            if _id in update_used_materials:
                used_material = used_materials.get(material__id=_id)
                used_material.amount = data["amount"]
                used_material.save()
            else:
                new_used_material.append(
                    UsedMaterial(
                        procedure=purchase_procedure,
                        material=stock_materials.get(id=_id),
                        amount=data["amount"],
                    )
                )
        UsedMaterial.objects.bulk_create(new_used_material)

    def update_used_materials(
        self,
        purchase_procedure: PurchaseProcedure,
        used_materials_data: list[dict[str, int]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        if used_materials_data is not None:
            if self.serializer.context["method"] == "PUT":
                self.put_used_materials(purchase_procedure, used_materials_data, used_materials)
            if self.serializer.context["method"] == "PATCH":
                self.patch_used_materials(purchase_procedure, used_materials_data, used_materials)

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[dict[str, int]] = self.serializer.validated_data.pop("materials")
        purchase_procedure = get_object_or_404(PurchaseProcedure, id=self.purchase_procedure_id)
        used_materials: QuerySet[UsedMaterial] = purchase_procedure.used_materials.all()
        if self.serializer.validated_data is not None:
            for key, value in self.serializer.validated_data.items():
                setattr(purchase_procedure, key, value)
            purchase_procedure.save()
        if used_materials_data is not None:
            self.update_used_materials(purchase_procedure, used_materials_data, used_materials)
        return purchase_procedure
