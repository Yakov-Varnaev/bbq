from django.urls import path

from .views import CompaniesViewSet

urlpatterns = [

    path('', CompaniesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>', CompaniesViewSet.as_view({'put': 'update', 'delete': 'destroy'}))

]
