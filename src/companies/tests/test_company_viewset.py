import pytest
from typing import Any, Callable

from freezegun import freeze_time
from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse
from django.utils import timezone

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from companies.api.serializers import CompanySerializer
from companies.models import Company

pytestmark = [
    pytest.mark.django_db,
]


def test_anonymous_user_cannot_create_company(as_anon: ApiClient, company_data: dict):
    url = reverse("api_v1:companies:company-list")
    as_anon.post(url, data=company_data, expected_status=status.HTTP_401_UNAUTHORIZED)  # type: ignore

    assert not Company.objects.exists()


@freeze_time()
def test_authenticated_user_can_create_company(as_user: ApiClient, company_data: dict, assert_company: Callable):
    now = timezone.now()
    url = reverse("api_v1:companies:company-list")
    as_user.post(url, data=company_data)  # type: ignore

    assert_company(company_data, created=now, modified=now)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_company_create_invalid_data(
    as_user: ApiClient, factory: FixtureFactory, invalid_fields: dict[str, Any], assert_company_doesnt_exist: Callable
):
    url = reverse("api_v1:companies:company-list")
    as_user.post(url, data=factory.company_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore

    assert_company_doesnt_exist()


@freeze_time()
def test_company_cannot_be_created_with_owner(as_user: ApiClient, factory: FixtureFactory, assert_company: Callable):
    """
    As DRF doesn't really give any api to disallow extra fields, we have to at least ensure
    that company owner is always set to the current user.
    """
    url = reverse("api_v1:companies:company-list")
    company_data = factory.company_data(owner=factory.user().id)
    as_user.post(url, data=company_data)  # type: ignore

    assert_company(company_data, owner=as_user.user)


@pytest.mark.parametrize(
    "client",
    [
        lf("as_anon"),
        lf("as_user"),
        lf("as_company_owner"),
    ],
)
def test_company_retrieve(client: ApiClient, company: Company):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    company_data = client.get(url)  # type: ignore

    assert CompanySerializer(company).data == company_data


@pytest.mark.parametrize(
    "client",
    [
        lf("as_anon"),
        lf("as_user"),
        lf("as_company_owner"),
    ],
)
def test_company_list(client: ApiClient, company: Company):
    url = reverse("api_v1:companies:company-list")
    companies_data = client.get(url)  # type: ignore

    assert companies_data["count"] == 1
    assert CompanySerializer([company], many=True).data == companies_data["results"]


def test_udpate_company(
    as_company_owner: ApiClient, company: Company, assert_company: Callable, factory: FixtureFactory
):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    company_data = factory.company_data()
    response_data = as_company_owner.put(url, data=company_data)  # type: ignore
    old_modified_ts = company.modified
    company.refresh_from_db()

    assert CompanySerializer(company).data == response_data
    assert company.modified > old_modified_ts
    assert_company(company_data, modified=company.modified)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_update_company_invalid_data(
    as_company_owner: ApiClient,
    company: Company,
    factory: FixtureFactory,
    invalid_fields: dict[str, Any],
):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    expected_data = CompanySerializer(company).data
    as_company_owner.put(url, data=factory.company_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore
    company.refresh_from_db()

    assert CompanySerializer(company).data == expected_data


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_non_owner_cannot_update_company(
    client: ApiClient, expected_status: int, company: Company, factory: FixtureFactory
):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    company_data = factory.company_data()
    client.put(url, data=company_data, expected_status=expected_status)  # type: ignore
    old_modified_ts = company.modified
    company.refresh_from_db()

    assert company.modified == old_modified_ts


def test_owner_can_delete_company(as_company_owner: ApiClient, company: Company, assert_company_doesnt_exist: Callable):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    as_company_owner.delete(url)  # type: ignore

    assert_company_doesnt_exist()


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_non_owner_cannot_delete_company(client: ApiClient, expected_status: int, company: Company):
    url = reverse("api_v1:companies:company-detail", kwargs={"pk": company.pk})
    client.delete(url, expected_status=expected_status)  # type: ignore
