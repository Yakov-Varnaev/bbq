from djoser import urls
from djoser.urls import jwt

from django.urls import include, path

app_name = "a12n"

urlpatterns = [
    path("", include(urls.urlpatterns + jwt.urlpatterns)),
]
