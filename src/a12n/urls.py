from djoser import urls  # type: ignore
from djoser.urls import jwt  # type: ignore

from django.urls import include, path

app_name = "a12n"

urlpatterns = [
    path("", include(urls.urlpatterns + jwt.urlpatterns)),
]
