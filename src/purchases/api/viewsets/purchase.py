from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from purchases.api.serializers import PurchaseSerializer


@extend_schema(tags=["purchases"])
class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsCompanyOwnerOrReadOnly]
