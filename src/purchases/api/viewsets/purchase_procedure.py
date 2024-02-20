from drf_spectacular.utils import extend_schema
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from django.db.models.query import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from purchases.api.serializers import PurchaseProcedureReadSerializer, PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure
from purchases.services.purchase_procedure import (
    PurchaseProcedureCreator,
    PurchaseProcedureDeleter,
    PurchaseProcedureUpdater,
)


@extend_schema(tags=["procedures-purchase"])
class PurchaseProcedureViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[PurchaseProcedure]:
        return (  # noqa: BLK100
            PurchaseProcedure.objects
            .point(self.kwargs["company_pk"], self.kwargs["point_pk"])
            .select_related("purchase", "procedure")
        )

    def get_serializer_class(self) -> type[PurchaseProcedureReadSerializer | PurchaseProcedureWriteSerializer]:
        if self.request.method in SAFE_METHODS:
            return PurchaseProcedureReadSerializer
        return PurchaseProcedureWriteSerializer

    def perform_create(self, serializer: type[PurchaseProcedureWriteSerializer]) -> None:
        return PurchaseProcedureCreator(serializer, self.kwargs["pk"])()

    def perform_update(self, serializer: type[PurchaseProcedureWriteSerializer]) -> None:
        return PurchaseProcedureUpdater(serializer, self.kwargs["pk"])()

    def perform_destroy(self, instance) -> None:
        return PurchaseProcedureDeleter(instance)()
