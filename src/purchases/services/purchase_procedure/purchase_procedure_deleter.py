from typing import Callable

from rest_framework.serializers import BaseSerializer

from django.db import transaction
from django.shortcuts import get_object_or_404

from app.services import BaseService
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure


class PurchaseProcedureDeleter(BaseService):
    def __init__(self, serializer: BaseSerializer[PurchaseProcedureWriteSerializer]) -> None:
        self.serializer = serializer

    def get_validators(self) -> list[Callable]:
        return [self.check_serializer_is_valid]

    def check_serializer_is_valid(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    @transaction.atomic
    def act(self) -> None:
        purchase_procedure = get_object_or_404(
            PurchaseProcedure, self.serializer.context["request"].query_params.get("pk")
        )
        purchase_procedure.used_materials.all().delete()
        purchase_procedure.delete()
