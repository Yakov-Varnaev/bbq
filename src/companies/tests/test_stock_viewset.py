import pytest

from pytest_lazyfixture import lazy_fixture as lf

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import RestPageAssertion
from companies.api.serializers import StockListSerializer, StockSerializer
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


def test_unauthorized_users_cannot_create_stock(
    as_point_non_managing_staff: ApiClient, company_point: Point, stock_data: dict
):
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-list",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
            },
        ),
        data=stock_data,
        expected_status=as_point_non_managing_staff.expected_status,  # type: ignore[attr-defined]
    )

    assert Stock.objects.count() == 0


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


def test_unauthorized_users_cannot_list_stocks(
    as_point_non_managing_staff: ApiClient, company_point: Point, factory: FixtureFactory
):
    factory.cycle(5).stock(point=company_point)
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-list",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
            },
        ),
        expected_status=as_point_non_managing_staff.expected_status,  # type: ignore[attr-defined]
    )


def test_authorized_users_can_retrieve_stock_detail(
    as_point_managing_staff: ApiClient, company_point: Point, stock: Stock
):
    stock_data = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": company_point.company.id,
                "point_pk": company_point.id,
                "pk": stock.id,
            },
        ),
    )

    assert stock_data == StockSerializer(stock).data


def test_unauthorized_users_cannot_retrieve_stock_detail(as_point_non_managing_staff: ApiClient, stock: Stock):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "pk": stock.id,
            },
        ),
        expected_status=as_point_non_managing_staff.expected_status,  # type: ignore[attr-defined]
    )


@pytest.mark.parametrize("status", map(lambda status: status[0], Stock.Status.choices))
def test_authorized_users_can_update_stock(
    as_point_managing_staff: ApiClient, company_point: Point, stock: Stock, factory: FixtureFactory, status: str
):
    stock_data = as_point_managing_staff.put(  # type: ignore[no-untyped-call]
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


def test_unauthorized_users_cannot_update_stock(as_point_non_managing_staff: ApiClient, stock: Stock, stock_data: dict):
    as_point_non_managing_staff.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "pk": stock.id,
            },
        ),
        data=stock_data,
        expected_status=as_point_non_managing_staff.expected_status,  # type: ignore[attr-defined]
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


def test_unauthorized_users_cannot_delete_stock(as_point_non_managing_staff: ApiClient, stock: Stock):
    as_point_non_managing_staff.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:stock-detail",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "pk": stock.id,
            },
        ),
        expected_status=as_point_non_managing_staff.expected_status,  # type: ignore[attr-defined]
    )

    assert Stock.objects.count() == 1
