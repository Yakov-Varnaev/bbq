from rest_framework import viewsets

from .models import CompaniesModel
from .permissions import *
from .serializers import CompaniesSerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CompaniesSerializer
    queryset = CompaniesModel.objects.all()

