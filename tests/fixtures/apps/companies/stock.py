import pytest

from app.testing.factory import FixtureFactory
from companies.models import MaterialType, Point, Stock, StockMaterial


@pytest.fixture
def stock_data(factory: FixtureFactory) -> dict:
    return factory.stock_data()


@pytest.fixture
def stock(factory: FixtureFactory, company_point: Point) -> dict:
    return factory.stock(point=company_point)


@pytest.fixture
def material_type(factory: FixtureFactory) -> MaterialType:
    return factory.material_type()


@pytest.fixture
def material_type_data(factory: FixtureFactory) -> dict:
    return factory.material_type_data()


@pytest.fixture
def material(factory: FixtureFactory) -> dict:
    return factory.material()


@pytest.fixture
def stock_material(factory: FixtureFactory, stock: Stock) -> StockMaterial:
    return factory.stock_material(stock=stock)
