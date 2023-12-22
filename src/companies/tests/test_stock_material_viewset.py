import pytest

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import ModelAssertion
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
