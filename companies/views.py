from rest_framework import viewsets

from .models import CompaniesModel
from .serializers import CompaniesSerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompaniesSerializer
    queryset = CompaniesModel.objects.all()
