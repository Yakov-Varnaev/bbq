from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers import EmployeeSerializer, PointCreateSerializer, PointSerializer
from companies.models import Point
from companies.services import EmployeeCreator


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
    def employees(self, *args: Any, **kwargs: Any) -> Response:
        serializer = EmployeeSerializer(data=self.request.data, context=self.get_serializer_context(*args, **kwargs))
        employee = EmployeeCreator(serializer)()
        return Response(EmployeeSerializer(employee).data)
