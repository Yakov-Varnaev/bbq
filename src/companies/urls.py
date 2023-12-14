from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter  # type: ignore[import]

from django.urls import include, path

from companies.api import viewsets

app_name = "companies"

router = SimpleRouter()
router.register("", viewsets.CompanyViewSet, basename="company")

company_router = NestedSimpleRouter(router, r"", lookup="company")
company_router.register("points", viewsets.PointViewSet, basename="point")

point_router = NestedSimpleRouter(company_router, "points", lookup="point")
point_router.register("departments", viewsets.DepartmentViewSet, basename="department")
point_router.register("stocks", viewsets.StockViewSet, basename="stock")

employee_router = NestedSimpleRouter(company_router, "points", lookup="point")
point_router.register("employees", viewsets.EmployeeViewSet, basename="employee")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(company_router.urls)),
    path("", include(point_router.urls)),
    path("", include(employee_router.urls)),
]
