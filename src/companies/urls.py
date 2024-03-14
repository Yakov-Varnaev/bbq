from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter  # type: ignore[import-untyped]

from django.urls import include, path

from companies.api import viewsets

app_name = "companies"

router = SimpleRouter()
router.register("companies", viewsets.CompanyViewSet, basename="company")
router.register("materials", viewsets.MaterialViewSet, basename="base-material")
router.register("material-types", viewsets.MaterialTypeViewSet, basename="material-types")
router.register("categories", viewsets.CategoryViewSet, basename="category")

company_router = NestedSimpleRouter(router, r"companies", lookup="company")
company_router.register("points", viewsets.PointViewSet, basename="point")

point_router = NestedSimpleRouter(company_router, "points", lookup="point")
point_router.register("departments", viewsets.DepartmentViewSet, basename="department")
point_router.register("stocks", viewsets.StockViewSet, basename="stock")
point_router.register("employees", viewsets.EmployeeViewSet, basename="employee")
point_router.register("materials", viewsets.ConsumableMaterialViewSet, basename="consumable-material")

department_router = NestedSimpleRouter(point_router, "departments", lookup="department")
department_router.register("procedures", viewsets.ProcedureViewSet, basename="procedure")

stock_router = NestedSimpleRouter(point_router, "stocks", lookup="stock")
stock_router.register("materials", viewsets.StockMaterialViewSet, basename="material")

employee_router = NestedSimpleRouter(point_router, "employees", lookup="employee")
employee_router.register("master-procedures", viewsets.MasterProcedureViewSet, basename="master-procedure")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(company_router.urls)),
    path("", include(point_router.urls)),
    path("", include(department_router.urls)),
    path("", include(stock_router.urls)),
    path("", include(employee_router.urls)),
]
