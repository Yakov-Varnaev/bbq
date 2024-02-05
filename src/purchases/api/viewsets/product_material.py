from drf_spectacular.utils import extend_schema
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from django.db.models.query import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from purchases.api.serializers import ProductMaterialCreateSerializer, ProductMaterialSerializer
from purchases.models.product_material import ProductMaterial


@extend_schema(tags=["products"])
class ProductMaterialViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[ProductMaterial]:
        return ProductMaterial.objects.point(self.kwargs["company_pk"], self.kwargs["point_pk"]).with_material_info()

    def get_serializer_class(self) -> type[ProductMaterialSerializer | ProductMaterialCreateSerializer]:
        if self.request.method in SAFE_METHODS:
            return ProductMaterialSerializer
        return ProductMaterialCreateSerializer
