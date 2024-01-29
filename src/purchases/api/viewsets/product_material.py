from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from django.db.models import QuerySet

from purchases.api.serializers.product_material import ProductMaterialCreateSerializer, ProductMaterialSerializer
from purchases.models import ProductMaterial

ProcedureSerialzierType = type[ProductMaterialSerializer] | type[ProductMaterialCreateSerializer]


@extend_schema(tags=["product materials"])
class ProductMaterialViewSet(viewsets.ModelViewSet):
    def get_queryset(self) -> QuerySet[ProductMaterial]:
        return ProductMaterial.objects.point(
            self.kwargs["company_pk"],
            self.kwargs["point_pk"],
        ).with_material_info()

    def get_serializer_class(self) -> ProcedureSerialzierType:
        if self.action in ["create", "update", "partial_update"]:
            return ProductMaterialCreateSerializer
        return ProductMaterialSerializer
