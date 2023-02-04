from rest_framework import viewsets
from .serializers import CompaniesSerializer
from .models import CompaniesModel


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompaniesSerializer
    queryset = CompaniesModel.objects.all()
