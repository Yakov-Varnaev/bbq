import pytest
from decimal import Decimal
from typing import Any

from app.types import ModelAssertion
from purchases.models.product_material import ProductMaterial


@pytest.fixture
def assert_product_material() -> ModelAssertion:
    def _assert_product_material(
        data: dict,
        **extra: Any,
    ):
        product_material = ProductMaterial.objects.get(id=data["id"])

        assert product_material.material.id == data.pop("material")
        assert product_material.price == Decimal(data.pop("price"))
        for field_name, expected_value in (data | extra).items():
            assert getattr(product_material, field_name) == expected_value

    return _assert_product_material
