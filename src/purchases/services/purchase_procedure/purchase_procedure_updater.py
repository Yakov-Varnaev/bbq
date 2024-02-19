from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from app.services import BaseService
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure, UsedMaterial


class PurchaseProcedureUpdater(BaseService):
    def __init__(self, serializer: BaseSerializer[PurchaseProcedureWriteSerializer]) -> None:
        self.serializer = serializer

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
        used_materials_data: list[dict[str, int]],
        used_materials: QuerySet[UsedMaterial],
    ) -> None:
        used_materials_id = used_materials.values_list("id", flat=True)
        new_used_materials: list[UsedMaterial] = []
        for data in used_materials_data:
            if data["material"] in used_materials_id:
                for key, value in data.items():
                    used_material = used_materials.get(id=data["material"])
                    setattr(used_material, key, value)
                used_material.save()
            else:
                new_used_materials.append(UsedMaterial(**data))
        UsedMaterial.objects.bulk_create(new_used_materials)

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
                self.patch_used_materials(used_materials_data, used_materials)

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[dict[str, int]] = self.serializer.validated_data.pop("materials")
        purchase_procedure = get_object_or_404(
            PurchaseProcedure, self.serializer.context["request"].query_params.get("pk")
        )
        used_materials: QuerySet[UsedMaterial] = purchase_procedure.used_materials.all()
        if self.serializer.validated_data is not None:
            for key, value in self.serializer.validated_data.items():
                setattr(purchase_procedure, key, value)
            purchase_procedure.save()
        if used_materials_data is not None:
            self.update_used_materials(purchase_procedure, used_materials_data, used_materials)
        return purchase_procedure
