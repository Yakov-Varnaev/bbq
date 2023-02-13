from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Company, CompanyPoint
from .permissions import IsCompanyPointOwnerOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    CompanyPointDetailSerializer,
    CompanyPointSerializer,
    CompanySerializer,
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
    queryset = CompanyPoint.objects.select_related('comapny')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyPointDetailSerializer
        return CompanyPointSerializer
