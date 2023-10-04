from rest_framework.viewsets import ModelViewSet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers.company import CompanySerializer
from companies.models import Company


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsCompanyOwnerOrReadOnly,
    ]
