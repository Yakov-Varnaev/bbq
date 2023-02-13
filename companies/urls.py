from django.urls import include, path
from rest_framework import routers

from .views import CompaniesViewSet

router = routers.SimpleRouter()
router.register('', CompaniesViewSet, basename='companies')

urlpatterns = [path('', include(router.urls))]
