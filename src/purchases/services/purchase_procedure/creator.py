from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction

from app.services import BaseService
from purchases.models import PurchaseProcedure, UsedMaterial


class PurchaseProcedureCreator(BaseService):
    def __init__(self, serializer: BaseSerializer) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def create_used_materials(
        self, purchase_procedure: PurchaseProcedure, used_materials_data: list[dict[str, int]]
    ) -> None:
        UsedMaterial.objects.bulk_create(
            [UsedMaterial(procedure=purchase_procedure, **data) for data in used_materials_data]
        )

    @transaction.atomic
    def act(self) -> PurchaseProcedure:
        used_materials_data: list[dict[str, int]] = self.serializer.validated_data.pop("materials")
        purchase_procedure: PurchaseProcedure = self.serializer.save()
        self.create_used_materials(purchase_procedure, used_materials_data)
        return purchase_procedure
