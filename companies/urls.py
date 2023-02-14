from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import (
    CompaniesViewSet,
    CompanyPointViewSet,
    DepartmentViewSet,
    EmployeeViewSet,
)

router = routers.SimpleRouter()
router.register('companies', CompaniesViewSet, basename='companies')
objects_router = NestedSimpleRouter(router, 'companies', lookup='company')
objects_router.register('points', CompanyPointViewSet, 'points')

employee_router = NestedSimpleRouter(objects_router, 'points', lookup='point')
employee_router.register('employees', EmployeeViewSet, 'employees')

departments_router = NestedSimpleRouter(objects_router, 'points', lookup='point')
departments_router.register('departmens', DepartmentViewSet, 'departments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(objects_router.urls)),
    path('', include(employee_router.urls)),
    path('', include(departments_router.urls)),
]
