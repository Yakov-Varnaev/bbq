import pytest

from app.testing.factory import FixtureFactory
from companies.models import Procedure, StockMaterial
from purchases.models import UsedMaterial
from purchases.types import UsedMaterialData


@pytest.fixture
def used_material_data(
    factory: FixtureFactory, procedure: Procedure, stock_material: StockMaterial
) -> UsedMaterialData:
    return factory.used_material_data(procedure=procedure, material=stock_material)


@pytest.fixture
def used_material(factory: FixtureFactory, procedure: Procedure, stock_material: StockMaterial) -> UsedMaterial:
    return factory.used_material(procedure=procedure, material=stock_material)
