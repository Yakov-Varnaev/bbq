import pytest
from typing import Any

from app.types import GenericModelAssertion
from purchases.models import ProductMaterial, Purchase, PurchaseProcedure, UsedMaterial
from purchases.types import ProductMaterialData, PurchaseData, PurchaseProcedureData, UsedMaterialData


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


class PurchaseProcedureAssert(GenericModelAssertion[PurchaseProcedureData]):
    def __call__(self, data: PurchaseProcedureData, **extra: Any) -> None:
        merged_data = data | extra
        purchase_procedure_id = merged_data["id"]
        assert isinstance(purchase_procedure_id, int)
        purchase_procedure = PurchaseProcedure.objects.get(id=purchase_procedure_id)
        assert purchase_procedure.procedure == merged_data.pop("procedure")
        assert purchase_procedure.purchase == merged_data.pop("purchase")

        for key, value in merged_data.items():
            check_result = getattr(purchase_procedure, key) == value
            assert check_result, f"{key} is not {value} but {getattr(purchase_procedure, key)}"


@pytest.fixture
def assert_purchase_procedure() -> GenericModelAssertion:
    return PurchaseProcedureAssert()


class UsedMaterialAssert(GenericModelAssertion[UsedMaterialData]):
    def __call__(self, data: UsedMaterialData, **extra: Any) -> None:
        merged_data = data | extra
        used_material_id = merged_data["id"]
        assert isinstance(used_material_id, int)
        used_material = UsedMaterial.objects.get(id=used_material_id)
        assert used_material.procedure == merged_data.pop("procedure")
        assert used_material.material == merged_data.pop("material")

        for key, value in merged_data.items():
            assert getattr(used_material, key) == value, f"{key} is not {value} but {getattr(used_material, key)}"


@pytest.fixture
def assert_used_material() -> GenericModelAssertion:
    return UsedMaterialAssert()
