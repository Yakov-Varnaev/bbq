import pytest

from app.testing.factory import FixtureFactory
from companies.models import StockMaterial
from purchases.models import PurchaseProcedure, UsedMaterial
from purchases.types import UsedMaterialData


@pytest.fixture
def used_material_data(
    factory: FixtureFactory, purchase_procedure: PurchaseProcedure, stock_material: StockMaterial
) -> UsedMaterialData:
    return factory.used_material_data(procedure=purchase_procedure.procedure, material=stock_material)


@pytest.fixture
def used_material(
    factory: FixtureFactory, purchase_procedure: PurchaseProcedure, stock_material: StockMaterial
) -> UsedMaterial:
    return factory.used_material(procedure=purchase_procedure.procedure, material=stock_material)


@pytest.fixture
def used_materials_data_without_procedure(factory: FixtureFactory) -> list[UsedMaterialData]:
    used_materials = factory.cycle(3).used_material_data(procedure=None)
    for used_material in used_materials:
        del used_material["procedure"]
    return used_materials


@pytest.fixture
def used_materials_data_without_procedure_and_not_unique(
    factory: FixtureFactory, stock_material: StockMaterial
) -> list[UsedMaterialData]:
    used_materials = factory.cycle(3).used_material_data(procedure=None, material=stock_material)
    for used_material in used_materials:
        del used_material["procedure"]
    return used_materials
