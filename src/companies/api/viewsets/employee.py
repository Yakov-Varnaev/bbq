from drf_spectacular.utils import extend_schema
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from django.db.models import QuerySet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers import EmployeeSerializer, MasterProcedureReadSerializer, MasterProcedureWriteSerializer
from companies.models import Employee, MasterProcedure


@extend_schema(tags=["employees"])
class EmployeeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrReadOnly]
    queryset = Employee.objects.none()  # for swagger schema
    serializer_class = EmployeeSerializer

    def get_queryset(self) -> QuerySet[Employee]:
        return Employee.objects.filter(
            departments__point__company_id=self.kwargs["company_pk"],
            departments__point_id=self.kwargs["point_pk"],
        )


@extend_schema(tags=["master-procedure"])
class MasterProcedureViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwnerOrReadOnly]
    queryset = MasterProcedure.objects.none()  # for swagger schema

    def get_serializer_class(self) -> type[MasterProcedureReadSerializer | MasterProcedureWriteSerializer]:
        if self.request.method in SAFE_METHODS:
            return MasterProcedureReadSerializer
        return MasterProcedureWriteSerializer

    def get_queryset(self) -> QuerySet[MasterProcedure]:
        return MasterProcedure.objects.filter(
            procedure__department__point__company_id=self.kwargs["company_pk"],
            procedure__department__point_id=self.kwargs["point_pk"],
            employee_id=self.kwargs["employee_pk"],
        )
