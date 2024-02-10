import pytest

from freezegun import freeze_time
from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from django.urls import reverse
from django.utils import timezone

from app.api.permissions import IsCompanyOwnerOrReadOnly
from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import ExistCheckAssertion, GenericModelAssertion, RestPageAssertion
from companies.api.serializers import PointSerializer
from companies.models import Company, Point
from companies.types import PointData

pytestmark = [pytest.mark.django_db]
non_company_owner_client_parametrize = (
    ("client", "status_code", "message"),
    [
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED, NotAuthenticated.default_detail),
        (lf("as_user"), status.HTTP_403_FORBIDDEN, IsCompanyOwnerOrReadOnly.message),
        (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN, IsCompanyOwnerOrReadOnly.message),
    ],
)


@freeze_time()
def test_company_owner_can_create_point(
    as_company_owner: ApiClient,
    company: Company,
    company_point_data: PointData,
    assert_company_point: GenericModelAssertion[PointData],
):
    point_data = as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-list", kwargs={"company_pk": company.id}), data=company_point_data
    )

    assert_company_point(
        company_point_data, id=point_data["id"], company=company, created=timezone.now(), modified=timezone.now()
    )


def test_point_cannot_be_created_with_non_existing_company(
    as_company_owner: ApiClient, company_point_data: PointData, assert_doesnt_exist: ExistCheckAssertion
):
    as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-list", kwargs={"company_pk": 999}),
        data=company_point_data,
        expected_status=status.HTTP_404_NOT_FOUND,
    )

    assert_doesnt_exist(Point)


@pytest.mark.parametrize(*non_company_owner_client_parametrize)
def test_non_owner_cannot_create_point(
    client: ApiClient,
    status_code: int,
    message: str,
    company: Company,
    company_point_data: PointData,
    assert_doesnt_exist: ExistCheckAssertion,
):
    response = client.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-list", kwargs={"company_pk": company.id}),
        data=company_point_data,
        expected_status=status_code,
    )

    assert_doesnt_exist(Point)
    assert response == {"detail": message}


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"address": ""},
    ],
)
def test_create_point_invalid_data(
    as_company_owner: ApiClient,
    company: Company,
    invalid_data: dict,
    factory: FixtureFactory,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-list", kwargs={"company_pk": company.id}),
        data=factory.company_point_data(**invalid_data),
        expected_status=status.HTTP_400_BAD_REQUEST,
    )

    assert_doesnt_exist(Point)


@pytest.mark.parametrize(
    "client",
    [
        lf("as_anon"),
        lf("as_user"),
        lf("as_company_owner"),
        lf("as_another_company_owner"),
    ],
)
def test_retrieve_point(client: ApiClient, company: Company, company_point: Point):
    point_data = client.get(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-detail", kwargs={"company_pk": company.id, "pk": company_point.id})
    )

    assert point_data == PointSerializer(company_point).data


def test_list_points(
    reader_client: ApiClient, company: Company, factory: FixtureFactory, assert_rest_page: RestPageAssertion
):
    points = sorted(factory.cycle(5).company_point(company=company), key=lambda p: p.address)
    points_data = reader_client.get(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-list", kwargs={"company_pk": company.id})
    )

    assert_rest_page(points_data, points, PointSerializer)


@freeze_time()
def test_owner_can_update_point(
    as_company_owner: ApiClient,
    company: Company,
    company_point: Point,
    assert_company_point: GenericModelAssertion[PointData],
):
    as_company_owner.patch(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-detail", kwargs={"company_pk": company.id, "pk": company_point.id}),
        data={"address": "new address"},
    )

    assert_company_point(
        {"address": "new address"},
        id=company_point.id,
        company=company,
        created=company_point.created,
        modified=timezone.now(),
    )


@pytest.mark.parametrize(*non_company_owner_client_parametrize)
def test_non_owner_cannot_update_point(
    client: ApiClient,
    status_code: int,
    message: str,
    company: Company,
    company_point: Point,
    assert_company_point: GenericModelAssertion[PointData],
):
    response = client.patch(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:point-detail",
            kwargs={"company_pk": company.id, "pk": company_point.id},
        ),
        data={"address": "new address"},
        expected_status=status_code,
    )

    assert_company_point(
        {"address": company_point.address}, id=company_point.id, company=company, modified=company_point.modified
    )
    assert response == {"detail": message}


def test_owner_can_delete_point(
    as_company_owner: ApiClient, company: Company, company_point: Point, assert_doesnt_exist: ExistCheckAssertion
):
    as_company_owner.delete(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-detail", kwargs={"company_pk": company.id, "pk": company_point.id})
    )

    assert_doesnt_exist(Point)


@pytest.mark.parametrize(*non_company_owner_client_parametrize)
def test_non_owner_cannot_delete_point(
    client: ApiClient,
    status_code: int,
    message: str,
    company: Company,
    company_point: Point,
    assert_exists: ExistCheckAssertion,
):
    response = client.delete(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:point-detail", kwargs={"company_pk": company.id, "pk": company_point.id}),
        expected_status=status_code,
    )

    assert_exists(Point, id=company_point.id)
    assert response == {"detail": message}
