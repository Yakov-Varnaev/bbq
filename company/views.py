from rest_framework import viewsets
from .serializers import CompanySerializer
from .models import CompanyModel


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = CompanyModel.objects.all()
