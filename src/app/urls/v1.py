from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from django.urls import include, path

app_name = "api_v1"
urlpatterns = [
    path("auth/", include("a12n.urls")),
    path("companies/", include("companies.urls", namespace="companies")),
    path("healthchecks/", include("django_healthchecks.urls")),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
]
