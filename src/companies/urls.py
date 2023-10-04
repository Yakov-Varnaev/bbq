from rest_framework.routers import SimpleRouter

from django.urls import include
from django.urls import path

from companies.api import viewsets

app_name = "companies"
router = SimpleRouter()

router.register("", viewsets.CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
]
