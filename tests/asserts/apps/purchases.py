import pytest
from typing import Any

from app.types import GenericModelAssertion
from purchases.models import ProductMaterial, Purchase
from purchases.types import ProductMaterialData, PurchaseData


class ProductMaterialAssert(GenericModelAssertion[ProductMaterialData]):
    def __call__(self, data: ProductMaterialData, **extra: Any) -> None:
        merged_data = data | extra
        product_id = merged_data["id"]
        assert isinstance(product_id, int)
        product = ProductMaterial.objects.get(id=product_id)

        for key, value in merged_data.items():
            assert getattr(product, key) == value, f"{key} is not {value} but {getattr(product, key)}"


@pytest.fixture
def assert_product_material() -> GenericModelAssertion:
    return ProductMaterialAssert()


class PurchaseAssert(GenericModelAssertion[PurchaseData]):
    def __call__(self, data: PurchaseData, **extra: Any) -> None:
        merged_data = data | extra
        purchase_id = merged_data["id"]
        assert isinstance(purchase_id, int)
        purchase = Purchase.objects.get(id=purchase_id)

        for key, value in merged_data.items():
            assert getattr(purchase, key) == value, f"{key} is not {value} but {getattr(purchase, key)}"


@pytest.fixture
def assert_purchase() -> GenericModelAssertion:
    return PurchaseAssert()
