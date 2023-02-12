from rest_framework import viewsets

from .models import CompaniesModel
from .permissions import IsAuthenticated, IsOwnerOrReadOnly
from .serializers import CompaniesSerializer


class CompaniesViewSet(viewsets.ModelViewSet):
    serializer_class = CompaniesSerializer
    queryset = CompaniesModel.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


