import pytest

from purchases.models.product_material import ProductMaterial

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("deleted_product_material")
def test_deleted_product_materials_are_not_included_by_default(
    product_material: ProductMaterial,
):
    products = ProductMaterial.objects.all()

    assert product_material in products


def test_allow_deleted_product_materials(
    product_material: ProductMaterial,
    deleted_product_material: ProductMaterial,
):
    products = ProductMaterial.allow_deleted.all()

    assert product_material in products
    assert deleted_product_material in products


def test_allow_deleted_with_deleted_only(
    product_material: ProductMaterial,
    deleted_product_material: ProductMaterial,
):
    products = ProductMaterial.allow_deleted.deleted()

    assert product_material not in products
    assert deleted_product_material in products


def test_allow_deleted_with_not_deleted_only(
    product_material: ProductMaterial,
    deleted_product_material: ProductMaterial,
):
    products = ProductMaterial.allow_deleted.not_deleted()

    assert product_material in products
    assert deleted_product_material not in products
