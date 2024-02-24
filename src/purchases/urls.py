from rest_framework.routers import SimpleRouter

from django.urls import include, path

from purchases.api import viewsets

app_name = "purchases"

router = SimpleRouter()

router.register(r"products", viewsets.ProductMaterialViewSet, basename="product")
router.register(r"purchases", viewsets.PurchaseViewSet, basename="purchase")
router.register(r"procedures-purchases", viewsets.PurchaseProcedureViewSet, basename="procedures-purchase")


urlpatterns = [
    path("companies/<int:company_pk>/points/<int:point_pk>/", include(router.urls)),
]
