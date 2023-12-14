from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.filters import CompanyFilterSet
from companies.api.serializers import CompanyCreateSerializer, CompanySerializer
from companies.models import Company


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    filterset_class = CompanyFilterSet

    def get_permissions(self) -> list[BasePermission]:
        if self.action == "create":
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly(), IsCompanyOwnerOrReadOnly()]

    def get_serializer_class(self) -> type[CompanySerializer | CompanyCreateSerializer]:
        if self.request.method in SAFE_METHODS:
            return CompanySerializer
        return CompanyCreateSerializer
