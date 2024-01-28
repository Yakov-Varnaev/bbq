import pytest

from app.testing.factory import FixtureFactory
from companies.models.stock import StockMaterial
from purchases.models.product_material import ProductMaterial


@pytest.fixture
def product_material(factory: FixtureFactory, stock_material: StockMaterial) -> ProductMaterial:
    return factory.product_material(material=stock_material)
