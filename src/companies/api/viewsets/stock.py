from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.db.models import QuerySet

from app.api.permissions import IsCompanyOwner
from companies.api.serializers import (
    MaterialSerializer,
    StockCreateSerializer,
    StockListSerializer,
    StockMaterialDetailedSerializer,
    StockMaterialSerializer,
    StockSerializer,
    StockUpdateSerializer,
)
from companies.models import Stock
from companies.models.stock import Material, StockMaterial


@extend_schema(tags=["materials"])
class MaterialViewSet(ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["brand", "name"]
    pagination_class = None


@extend_schema(tags=["stocks"])
class StockViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwner]
    queryset = Stock.objects.all()

    def get_queryset(self) -> QuerySet[Stock]:
        return Stock.objects.detailed().order_by("-date")

    def get_serializer_class(self) -> type[BaseSerializer[Stock]]:
        serializers = {
            "list": StockListSerializer,
            "create": StockCreateSerializer,
            "update": StockUpdateSerializer,
        }
        return serializers.get(self.action, StockSerializer)


@extend_schema(tags=["stocks"])
class StockMaterialViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwner]
    queryset = StockMaterial.objects.select_related("material", "material__kind")

    def get_serializer_class(self) -> type[BaseSerializer[StockMaterial]]:
        if self.action in ["list", "retrieve"]:
            return StockMaterialDetailedSerializer
        return StockMaterialSerializer
