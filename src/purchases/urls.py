from rest_framework.routers import SimpleRouter

from django.urls import include, path

from purchases.api import viewsets

router = SimpleRouter()
router.register("products", viewsets.ProductMaterialViewSet, basename="products")

app_name = "purchases"

urlpatterns = [
    path("companies/<int:company_id>/points/<int:point_id>/", include(router.urls)),
]
