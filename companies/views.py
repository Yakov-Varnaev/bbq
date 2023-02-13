from django.utils import timezone
from rest_framework import viewsets

from .models import Company
from .permissions import IsAuthenticated, IsOwnerOrReadOnly
from .serializers import CompanySerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(time_updated=timezone.now())
