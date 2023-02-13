from django.urls import include, path
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from .views import CompaniesViewSet, CompanyPointViewSet

router = routers.SimpleRouter()
router.register('companies', CompaniesViewSet, basename='companies')
objects_router = NestedSimpleRouter(router, r'companies', lookup='company')
objects_router.register('points', CompanyPointViewSet, 'points')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(objects_router.urls)),
]
