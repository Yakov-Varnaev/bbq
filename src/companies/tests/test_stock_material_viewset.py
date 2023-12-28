import pytest

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import ModelAssertion, RestPageAssertion
from companies.api.serializers import StockMaterialDetailedSerializer
from companies.models.stock import Material, Stock, StockMaterial

pytestmark = pytest.mark.django_db

unauthorized_users = [
    (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN),
    (lf("as_user"), status.HTTP_403_FORBIDDEN),
    (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
]


def test_authorized_users_can_add_stock_material(
    as_point_managing_staff: ApiClient,
    stock: Stock,
    material: Material,
    factory: FixtureFactory,
    assert_stock_material: ModelAssertion,
):
    material_data = factory.stock_material_data(material=material)
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-list",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "stock_pk": stock.id,
            },
        ),
        data=material_data,
    )

    assert_stock_material(material_data, stock=stock)


@pytest.mark.parametrize(
    ("client", "expected_status"),
    unauthorized_users,
)
def test_unauthorized_users_cannot_add_stock_material(
    client: ApiClient,
    expected_status: int,
    stock: Stock,
    material: Material,
    factory: FixtureFactory,
):
    material_data = factory.stock_material_data(material=material)
    client.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-list",
            kwargs={
                "company_pk": stock.point.company.id,
                "point_pk": stock.point.id,
                "stock_pk": stock.id,
            },
        ),
        data=material_data,
        expected_status=expected_status,
    )

    assert StockMaterial.objects.count() == 0


def test_authorized_users_can_edit_stock_material(
    as_point_managing_staff: ApiClient,
    stock_material: StockMaterial,
    factory: FixtureFactory,
    assert_stock_material: ModelAssertion,
):
    material_data = factory.stock_material_data(material=stock_material.material)
    as_point_managing_staff.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        ),
        data=material_data,
    )
    stock_material.refresh_from_db()

    assert_stock_material(material_data)


@pytest.mark.parametrize(
    ("client", "expected_status"),
    unauthorized_users,
)
def test_unauthorized_users_cannot_edit_stock_material(
    client: ApiClient,
    expected_status: int,
    stock_material: StockMaterial,
    factory: FixtureFactory,
):
    material_data = factory.stock_material_data(material=stock_material.material)
    client.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        ),
        data=material_data,
        expected_status=expected_status,
    )
    stock_from_db = StockMaterial.objects.get(id=stock_material.id)

    assert stock_from_db == stock_material
    assert StockMaterial.objects.count() == 1


def test_authorized_users_can_retrieve_stock_material(
    as_point_managing_staff: ApiClient,
    stock_material: StockMaterial,
):
    stock_material_data = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        )
    )

    assert stock_material_data == StockMaterialDetailedSerializer(stock_material).data


@pytest.mark.parametrize(
    ("client", "expected_status"),
    unauthorized_users,
)
def test_unauthorized_users_cannot_retrieve_stock_material(
    client: ApiClient,
    expected_status: int,
    stock_material: StockMaterial,
):
    client.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        ),
        expected_status=expected_status,
    )


def test_authorized_users_can_list_stock_materials(
    as_point_managing_staff: ApiClient, stock_material: StockMaterial, assert_rest_page: RestPageAssertion
):
    stock_material_data = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-list",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
            },
        )
    )

    assert_rest_page(stock_material_data, StockMaterial.objects.all(), StockMaterialDetailedSerializer)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("client", "expected_status"),
    unauthorized_users,
)
def test_unauthorized_users_cannot_list_stock_materials(
    client: ApiClient,
    expected_status: int,
    stock_material: StockMaterial,
):
    client.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-list",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
            },
        ),
        expected_status=expected_status,
    )


def test_authorized_users_can_delete_stock_material(
    as_point_managing_staff: ApiClient,
    stock_material: StockMaterial,
):
    as_point_managing_staff.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        ),
    )

    assert StockMaterial.objects.count() == 0


@pytest.mark.parametrize(
    ("client", "expected_status"),
    unauthorized_users,
)
def test_unauthorized_users_cannot_delete_stock_material(
    client: ApiClient,
    expected_status: int,
    stock_material: StockMaterial,
):
    client.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:material-detail",
            kwargs={
                "company_pk": stock_material.stock.point.company.id,
                "point_pk": stock_material.stock.point.id,
                "stock_pk": stock_material.stock.id,
                "pk": stock_material.id,
            },
        ),
        expected_status=expected_status,
    )

    assert StockMaterial.objects.count() == 1
