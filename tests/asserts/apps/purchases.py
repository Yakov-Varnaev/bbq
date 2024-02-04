import pytest
from typing import Any

from app.types import GenericModelAssertion
from purchases.models.product_material import ProductMaterial
from purchases.types import ProductMaterialData


class ProductMaterialAssert(GenericModelAssertion[ProductMaterialData]):
    def __call__(self, data: ProductMaterialData, **extra: Any) -> None:
        merged_data = data | extra
        product_id = merged_data["id"]
        assert isinstance(product_id, int)
        product = ProductMaterial.objects.get(id=product_id)

        for key, value in data.items():
            assert getattr(product, key) == value, f"{key} is not {value} but {getattr(product, key)}"


@pytest.fixture
def assert_product_material() -> GenericModelAssertion:
    return ProductMaterialAssert()
