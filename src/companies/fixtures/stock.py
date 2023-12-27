import pytest

from app.testing.factory import FixtureFactory
from companies.models.point import Point
from companies.models.stock import Stock, StockMaterial


@pytest.fixture
def stock_data(factory: FixtureFactory) -> dict:
    return factory.stock_data()


@pytest.fixture
def stock(factory: FixtureFactory, company_point: Point) -> dict:
    return factory.stock(point=company_point)


@pytest.fixture
def material(factory: FixtureFactory) -> dict:
    return factory.material()


@pytest.fixture
def stock_material(factory: FixtureFactory, stock: Stock) -> StockMaterial:
    return factory.stock_material(stock=stock)
