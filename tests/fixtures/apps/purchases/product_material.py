import pytest

from app.testing.factory import FixtureFactory
from companies.models.stock import StockMaterial
from purchases.models.product_material import ProductMaterial
from purchases.types import ProductMaterialData


@pytest.fixture
def product_material_data(factory: FixtureFactory, stock_material: StockMaterial) -> ProductMaterialData:
    return factory.product_material_data(material=stock_material)


@pytest.fixture
def product_material(factory: FixtureFactory, stock_material: StockMaterial) -> ProductMaterial:
    return factory.product_material(material=stock_material)
