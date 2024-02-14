from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from django.db.models.query import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from purchases.api.serializers import PurchaseSerializer
from purchases.models import Purchase


@extend_schema(tags=["purchases"])
class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsCompanyOwnerOrReadOnly]

    def get_queryset(self) -> QuerySet[Purchase]:
        return Purchase.objects.point(self.kwargs["company_pk"], self.kwargs["point_pk"])
