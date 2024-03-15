from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import F, QuerySet, Sum, OuterRef, Subquery
from django.db.models.functions import JSONObject, TruncDate
from django.contrib.postgres.aggregates import JSONBAgg, ArrayAgg

from app.api.permissions import IsCompanyOwner, IsCompanyOwnerOrReadOnly
from companies.api.serializers import (
    ConsumableMateriaSerializer,
    EmployeeSerializer,
    PointCreateSerializer,
    PointSerializer,
)
from companies.models import Point, StockMaterial
from companies.services import EmployeeCreator
from purchases.models import UsedMaterial


@extend_schema(tags=["points"])
class PointViewSet(ModelViewSet):
    queryset = Point.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCompanyOwnerOrReadOnly,
    ]

    def get_serializer_class(self) -> type[PointSerializer | PointCreateSerializer | EmployeeSerializer]:
        if self.action == "employees":
            return EmployeeSerializer
        if self.action == "create":
            return PointCreateSerializer
        return PointSerializer

    @extend_schema(request=EmployeeSerializer, responses={200: EmployeeSerializer})
    @action(detail=True, methods=["post"])
    def add_employees(self, *args: Any, **kwargs: Any) -> Response:
        serializer = EmployeeSerializer(data=self.request.data, context=self.get_serializer_context(*args, **kwargs))
        employee = EmployeeCreator(serializer)()
        return Response(EmployeeSerializer(employee).data)


class ConsumableMaterialViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = ConsumableMateriaSerializer
    # permission_classes = [IsCompanyOwner]

    def get_queryset(self) -> QuerySet:
        queryset = (
            StockMaterial.objects.prefetch_related("material")
            .filter(
                stock__point__company__id=self.kwargs["company_pk"],
                stock__point__id=self.kwargs["point_pk"],
            )
        )
        print('queryset -', queryset)
        stocks = (
            queryset
            .order_by("stock__date")
            .values("material", date=F("stock__date"))
            .annotate(amount=Sum("quantity"))
        )
        print('stocks -', stocks)
        usage = (
            UsedMaterial.objects
            .with_material_info()
            .point(
                self.kwargs["company_pk"], self.kwargs["point_pk"]
            )
            .annotate(date=TruncDate("modified"))
            .order_by("date")
            .values("material", "date")
            .annotate(amount=Sum("amount"))
        )
        print('usage -', usage)
        return queryset

