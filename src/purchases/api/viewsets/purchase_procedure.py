from drf_spectacular.utils import extend_schema
from rest_framework.permissions import SAFE_METHODS
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from django.db.models.query import QuerySet

from app.api.permissions import IsCompanyOwner
from purchases.api.serializers import PurchaseProcedureReadSerializer, PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure
from purchases.services.purchase_procedure import (
    PurchaseProcedureCreator,
    PurchaseProcedureDeleter,
    PurchaseProcedureUpdater,
)


@extend_schema(tags=["procedures-purchase"])
class PurchaseProcedureViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwner]

    def get_queryset(self) -> QuerySet[PurchaseProcedure]:
        return PurchaseProcedure.objects.point(self.kwargs["company_pk"], self.kwargs["point_pk"])

    def get_serializer_class(self) -> type[PurchaseProcedureReadSerializer | PurchaseProcedureWriteSerializer]:
        if self.request.method in SAFE_METHODS:
            return PurchaseProcedureReadSerializer
        return PurchaseProcedureWriteSerializer

    def perform_create(self, serializer: BaseSerializer[PurchaseProcedureWriteSerializer]) -> None:
        PurchaseProcedureCreator(serializer)()

    def perform_update(self, serializer: BaseSerializer[PurchaseProcedureWriteSerializer]) -> None:
        PurchaseProcedureUpdater(serializer, self.kwargs["pk"])()

    def perform_destroy(self, instance: PurchaseProcedure) -> None:
        PurchaseProcedureDeleter(instance)()
