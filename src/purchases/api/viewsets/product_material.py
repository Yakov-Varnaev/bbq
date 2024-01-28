from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from django.db.models import QuerySet

from purchases.api.serializers.product_material import ProductMaterialCreateSerializer, ProductMaterialSerializer
from purchases.models import ProductMaterial


@extend_schema(tags=["product materials"])
class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterial.objects.all()

    def get_queryset(self) -> QuerySet[ProductMaterial]:
        return ProductMaterial.objects.get_queryset().point(self.kwargs["company_id"], self.kwargs["point_id"])

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductMaterialCreateSerializer
        return ProductMaterialSerializer
