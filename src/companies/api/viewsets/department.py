from drf_spectacular.utils import extend_schema
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet

from app.api.permissions import CreateOrReadOnly, IsCompanyOwnerOrReadOnly, IsSuperUser
from companies.api.serializers import (
    CategorySerializer,
    DepartmentCreateSerialzier,
    DepartmentSerializer,
    ProcedureCreateUpdateSerialzier,
    ProcedureSerializer,
)
from companies.models import Category, Department, Procedure
from companies.services import CategoryCreator


@extend_schema(tags=["departments"])
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


@extend_schema(tags=["categories"])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser | IsAuthenticatedOrReadOnly & CreateOrReadOnly]

    def perform_create(self, serializer: BaseSerializer[CategorySerializer]) -> None:
        CategoryCreator(serializer)()


@extend_schema(tags=["procedure"])
class ProcedureViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrReadOnly]

    def get_serializer_class(self) -> type[ProcedureSerializer | ProcedureCreateUpdateSerialzier]:
        if self.request.method in SAFE_METHODS:
            return ProcedureSerializer
        return ProcedureCreateUpdateSerialzier

    def get_queryset(self) -> QuerySet[Procedure]:
        return Procedure.objects.filter(
            department__point__company_id=self.kwargs["company_pk"],
            department__point__id=self.kwargs["point_pk"],
            department_id=self.kwargs["department_pk"],
        )
