from django.urls import path
from .views import CompanyViewSet


urlpatterns = [

    path('', CompanyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:pk>', CompanyViewSet.as_view({'put': 'update', 'delete': 'destroy'}))

]
