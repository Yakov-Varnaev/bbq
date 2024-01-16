from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers import (
    DepartmentCreateSerialzier,
    DepartmentSerializer,
    ProcedureCreateUpdateSerialzier,
    ProcedureSerializer,
)
from companies.models import Department, Procedure


@extend_schema(
    tags=["departments"],
    parameters=[OpenApiParameter("company_pk", OpenApiTypes.INT, OpenApiParameter.PATH)],
)
class DepartmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrReadOnly]
    queryset = Department.objects.none()  # for swagger schema

    def get_serializer_class(self) -> type[DepartmentCreateSerialzier | DepartmentSerializer]:
        if self.action == "create":
            return DepartmentCreateSerialzier
        return DepartmentSerializer

    def get_queryset(self) -> QuerySet[Department]:
        return Department.objects.filter(
            point__company_id=self.kwargs["company_pk"],
            point_id=self.kwargs["point_pk"],
        )


@extend_schema(
    tags=["procedure"],
    parameters=[
        OpenApiParameter("company_pk", OpenApiTypes.INT, OpenApiParameter.PATH),
        OpenApiParameter("point_pk", OpenApiTypes.INT, OpenApiParameter.PATH),
        OpenApiParameter("department_pk", OpenApiTypes.INT, OpenApiParameter.PATH),
    ],
)
class ProcedureViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrReadOnly]

    def get_serializer_class(self) -> type[ProcedureSerializer | ProcedureCreateUpdateSerialzier]:
        if self.request.method in SAFE_METHODS:
            return ProcedureSerializer
        return ProcedureCreateUpdateSerialzier

    def get_queryset(self) -> QuerySet[Procedure]:
        return Procedure.objects.filter(
            department___point__company_id=self.kwargs["company_pk"],
            department___point_id=self.kwargs["point_pk"],
            department_id=self.kwargs["department_pk"],
        )
