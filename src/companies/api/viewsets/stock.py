from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.db.models import QuerySet

from app.api.permissions import CreateOrReadOnly, IsCompanyOwner, IsSuperUser
from companies.api.serializers import (
    MaterialSerializer,
    MaterialTypeSerializer,
    StockCreateSerializer,
    StockListSerializer,
    StockMaterialDetailedSerializer,
    StockMaterialSerializer,
    StockSerializer,
    StockUpdateSerializer,
)
from companies.models import Material, MaterialType, Stock, StockMaterial
from companies.services import MaterialTypeCreator


@extend_schema(tags=["materials"])
class MaterialViewSet(ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["brand", "name"]
    pagination_class = None


@extend_schema(tags=["types-of-materials"])
class MaterialTypeViewSet(ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer
    permission_classes = [IsSuperUser | IsAuthenticatedOrReadOnly & CreateOrReadOnly]

    def perform_create(self, serializer: BaseSerializer[MaterialTypeSerializer]) -> None:
        MaterialTypeCreator(serializer)()


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
