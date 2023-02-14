from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Company, CompanyPoint, Department, Employee
from .permissions import HasOwnerPermissionOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    CompanyPointDetailSerializer,
    CompanyPointSerializer,
    CompanySerializer,
    DepartmentDetailSerializer,
    DepartmentSerializer,
    EmployeeDetailSerializer,
    EmployeeSerializer,
)


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(time_updated=timezone.now())


@extend_schema(tags=['company points'])
class CompanyPointViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasOwnerPermissionOrReadOnly]
    queryset = CompanyPoint.objects.select_related('company')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyPointDetailSerializer
        return CompanyPointSerializer


@extend_schema(tags=['departments'])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [HasOwnerPermissionOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        return DepartmentSerializer


@extend_schema(tags=['employees'])
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [HasOwnerPermissionOrReadOnly]

    def get_queryset(self):
        if self.action == 'retrieve':
            return Employee.objects.select_related('point', 'point__company')
        return Employee.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer
