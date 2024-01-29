import pytest

from django.urls import reverse

from app.testing import ApiClient
from app.types import ModelAssertion, RestPageAssertion
from companies.models.point import Point
from purchases.api.serializers import ProductMaterialSerializer
from purchases.models.product_material import ProductMaterial

pytestmark = pytest.mark.django_db


# test anyone can read
# test deleted objects are not returned
# test only point managing staff can create/update/delete
# test cannot create duplicated of same product material
# test duplicated product material can be created if previous one is marked as deleted
# test product material is not entirely deleted from db on delete


def get_list_url(point: Point) -> str:
    return reverse(
        "api_v1:purchases:products-list",
        kwargs={
            "company_pk": point.company_id,
            "point_pk": point.id,
        },
    )


def test_point_managing_staff_can_create_product_material(
    as_point_managing_staff: ApiClient, product_material_data: dict, assert_product_material: ModelAssertion
):
    point = Point.objects.get()
    response = as_point_managing_staff.post(get_list_url(point), data=product_material_data)  # type: ignore[no-untyped-call]

    assert_product_material(response)


@pytest.mark.usefixtures("deleted_product_material")
def test_deleted_products_are_not_listed(
    as_anon: ApiClient, product_material: ProductMaterial, assert_rest_page: RestPageAssertion
):
    point = Point.objects.get()
    response = as_anon.get(get_list_url(point))  # type: ignore[no-untyped-call]
    materials = ProductMaterial.objects.with_material_info().filter(id=product_material.id)

    assert_rest_page(response, materials, ProductMaterialSerializer)
