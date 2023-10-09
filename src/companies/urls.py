from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter  # type: ignore[import]

from django.urls import include, path

from companies.api import viewsets

app_name = "companies"
router = SimpleRouter()

router.register("", viewsets.CompanyViewSet, basename="company")
point_router = NestedSimpleRouter(router, r"", lookup="company")
point_router.register("points", viewsets.PointViewSet, basename="point")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(point_router.urls)),
]
