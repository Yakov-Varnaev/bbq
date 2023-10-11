from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from app.api.permissions import IsCompanyOwnerOrReadOnly
from companies.api.serializers import PointCreateSerializer, PointSerializer
from companies.models import Point


@extend_schema(tags=["points"])
class PointViewSet(ModelViewSet):
    queryset = Point.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsCompanyOwnerOrReadOnly,
    ]

    def get_serializer_class(self) -> type[PointSerializer | PointCreateSerializer]:
        if self.action == "create":
            return PointCreateSerializer
        return PointSerializer
