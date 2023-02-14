from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Company, CompanyPoint, Employee
from .permissions import AllowedToEmploy, IsCompanyPointOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    CompanyPointDetailSerializer,
    CompanyPointSerializer,
    CompanySerializer,
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


@extend_schema(tags=['company point'])
class CompanyPointViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsCompanyPointOwnerOrReadOnly]
    queryset = CompanyPoint.objects.select_related('company')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyPointDetailSerializer
        return CompanyPointSerializer


@extend_schema(tags=['employees'])
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowedToEmploy]

    def get_queryset(self):
        if self.action == 'retrieve':
            return Employee.objects.select_related('point', 'point__company')
        return Employee.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer
