from drf_spectacular.utils import extend_schema
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers import StockCreateSerializer, StockListSerializer, StockSerializer
from companies.api.serializers.stock import StockUpdateSerializer
from companies.models import Stock


@extend_schema(tags=["sotcks"])
class StockViewSet(ModelViewSet):
    permission_classes = [IsCompanyOwnerOrReadOnly]
    queryset = Stock.objects.all()

    def get_queryset(self) -> QuerySet[Stock]:
        return Stock.objects.detailed()

    def get_serializer_class(self) -> type[BaseSerializer[Stock]]:
        match self.action:
            case "list":
                return StockListSerializer
            case "create":
                return StockCreateSerializer
            case "update":
                return StockUpdateSerializer
            case _:
                return StockSerializer
