import pytest

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing.api import ApiClient
from companies.api.serializers.company import CompanySerializer
from companies.models.company import Company

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    "client",
    [
        lf("as_anon"),
        lf("as_user"),
        lf("owner_client"),
    ],
)
def test_company_retrieve(client: ApiClient, company: Company):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    company_data = client.get(url)

    assert CompanySerializer(company).data == company_data
