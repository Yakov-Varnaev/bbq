from rest_framework.routers import SimpleRouter

from django.urls import include, path

from purchases.api import viewsets

app_name = "purchases"

router = SimpleRouter()

router.register(r"products", viewsets.ProductMaterialViewSet, basename="product")

urlpatterns = [
    path("companies/<int:company_pk>/points/<int:point_pk>/", include(router.urls)),
]