import pytest

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import RestPageAssertion
from companies.api.serializers import StockSerializer
from companies.api.serializers.stock import StockListSerializer
from companies.models import Stock
from companies.models.point import Point

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client",
    [
        lf("as_company_owner"),
    ],
)
def test_authorized_users_can_create_stock(client: ApiClient, company_point: Point, stock_data: dict):
    stock_data = client.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-list",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
            },
        ),
        data=stock_data,
    )
    stock = Stock.objects.get(id=stock_data["id"])

    assert stock_data == StockSerializer(stock).data
    assert stock.status == Stock.Status.DRAFT
    assert stock.point == company_point


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN),
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_unauthorized_users_cannot_create_stock(
    client: ApiClient, expected_status: int, company_point: Point, stock_data: dict
):
    client.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-list",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
            },
        ),
        data=stock_data,
        expected_status=expected_status,
    )

    assert Stock.objects.count() == 0


@pytest.mark.parametrize(
    "client",
    [
        lf("as_company_owner"),
    ],
)
@pytest.mark.parametrize("status", map(lambda status: status[0], Stock.Status.choices))
def test_authorized_users_can_update_stock(
    client: ApiClient, company_point: Point, stock: Stock, factory: FixtureFactory, status: str
):
    stock_data = client.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
                "pk": stock.id,
            },
        ),
        data=factory.stock_data(status=status),
    )
    stock.refresh_from_db()

    assert stock_data == StockSerializer(stock).data
    assert stock.status == status
    assert stock.point == company_point


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN),
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_unauthorized_users_cannot_update_stock(
    client: ApiClient, expected_status: int, stock: Stock, stock_data: dict
):
    client.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "pk": stock.id,
            },
        ),
        data=stock_data,
        expected_status=expected_status,
    )

    stock.refresh_from_db()

    assert stock.status == Stock.Status.DRAFT


@pytest.mark.parametrize(
    "client",
    [
        lf("as_company_owner"),
    ],
)
def test_authorized_users_can_delete_stock(client: ApiClient, company_point: Point, stock: Stock):
    client.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
                "pk": stock.id,
            },
        ),
    )

    assert Stock.objects.count() == 0


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN),
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_unauthorized_users_cannot_delete_stock(client: ApiClient, expected_status: int, stock: Stock):
    client.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "pk": stock.id,
            },
        ),
        expected_status=expected_status,
    )

    assert Stock.objects.count() == 1


@pytest.mark.parametrize(
    "client",
    [
        lf("as_company_owner"),
    ],
)
def test_authorized_users_can_list_stocks(
    client: ApiClient, company_point: Point, assert_rest_page: RestPageAssertion, factory: FixtureFactory
):
    factory.cycle(5).stock(point=company_point)
    stocks = Stock.objects.detailed().order_by("-date")
    stocks_data = client.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-list",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
            },
        ),
    )

    assert_rest_page(stocks_data, stocks, StockListSerializer, None, None)
