import pytest

from django.urls import reverse
from django.utils import timezone

from app.testing.api import ApiClient, StatusApiClient
from app.types import ExistCheckAssertion, ModelAssertion, RestPageAssertion
from companies.models.stock import StockMaterial
from purchases.api.serializers import ProductMaterialSerializer
from purchases.models.product_material import ProductMaterial
from purchases.types import ProductMaterialData

pytestmark = pytest.mark.django_db


@pytest.mark.freeze_time("2022-01-01")
def test_point_managing_staff_can_create(
    as_point_managing_staff: ApiClient,
    product_material_data: ProductMaterialData,
    stock_material: StockMaterial,
    assert_product_material: ModelAssertion,
):
    point = stock_material.stock.point
    url = reverse("api_v1:purchases:product-list", kwargs={"company_pk": point.company.pk, "point_pk": point.pk})
    product_data = as_point_managing_staff.post(url, data=product_material_data)  # type: ignore[no-untyped-call]
    product_material = ProductMaterial.objects.get(pk=product_data["id"])
    now = timezone.now()

    assert_product_material(
        product_material_data,  # type: ignore[arg-type]
        material=stock_material,
        id=product_material.pk,
        created=now,
        modified=now,
        archived=None,
    )


def test_non_point_managing_staff_cannot_create(
    as_point_non_managing_staff: StatusApiClient,
    product_material_data: ProductMaterialData,
    stock_material: StockMaterial,
    assert_doesnt_exist: ExistCheckAssertion,
):
    client = as_point_non_managing_staff
    point = stock_material.stock.point
    url = reverse("api_v1:purchases:product-list", kwargs={"company_pk": point.company.pk, "point_pk": point.pk})
    client.post(  # type: ignore[no-untyped-call]
        url,
        data=product_material_data,
        expected_status=client.expected_status,
    )

    assert_doesnt_exist(ProductMaterial)


def test_retrieve(reader_client: ApiClient, product_material: ProductMaterial):
    product_material_data = reader_client.get(product_material.get_absolute_url())  # type: ignore[no-untyped-call]
    product_material = ProductMaterial.objects.with_material_info().get(pk=product_material.pk)

    assert product_material_data == ProductMaterialSerializer(product_material).data


def test_list(reader_client: ApiClient, product_material: ProductMaterial, assert_rest_page: RestPageAssertion):
    point = product_material.material.stock.point
    url = reverse("api_v1:purchases:product-list", kwargs={"company_pk": point.company.pk, "point_pk": point.pk})
    product_material_data = reader_client.get(url)  # type: ignore[no-untyped-call]
    products = ProductMaterial.objects.point(point.company.pk, point.pk).with_material_info()

    assert_rest_page(product_material_data, products, ProductMaterialSerializer)


@pytest.mark.freeze_time("2022-01-01")
def test_point_managing_staff_can_update(
    as_point_managing_staff: ApiClient,
    product_material: ProductMaterial,
    product_material_data: ProductMaterialData,
    assert_product_material: ModelAssertion,
):
    client = as_point_managing_staff
    url = product_material.get_absolute_url()
    product_material_data["price"] = product_material_data["price"] + 1
    client.put(url, data=product_material_data)  # type: ignore[no-untyped-call]

    assert_product_material(
        product_material_data,  # type: ignore[arg-type]
        material=product_material.material,
        id=product_material.pk,
        created=product_material.created,
        modified=timezone.now(),
        archived=None,
    )


@pytest.mark.skip("not implemented")
def test_product_material_price_cannot_be_updated_if_there_are_sales():
    pass


def test_non_point_managing_staff_cannot_update(
    as_point_non_managing_staff: StatusApiClient,
    product_material: ProductMaterial,
    product_material_data: ProductMaterialData,
    assert_product_material: ModelAssertion,
):
    client = as_point_non_managing_staff
    url = product_material.get_absolute_url()
    client.put(  # type: ignore[no-untyped-call]
        url,
        data=product_material_data,
        expected_status=client.expected_status,
    )

    product_material.refresh_from_db()
    assert_product_material(
        {},
        id=product_material.pk,
        price=product_material.price,
        material=product_material.material,
        created=product_material.created,
        modified=product_material.modified,
        archived=product_material.archived,
    )


def test_point_managing_staff_can_delete(
    as_point_managing_staff: ApiClient,
    product_material: ProductMaterial,
    assert_doesnt_exist: ExistCheckAssertion,
):
    client = as_point_managing_staff
    url = product_material.get_absolute_url()
    client.delete(url)  # type: ignore[no-untyped-call]

    assert_doesnt_exist(ProductMaterial)


@pytest.mark.skip("not implemented")
def test_product_material_archive_if_there_are_sales():
    pass
