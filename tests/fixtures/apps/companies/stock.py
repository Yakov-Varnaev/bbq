import pytest

from app.testing.types import FactoryProtocol
from companies.models import MaterialType, Point, Stock, StockMaterial


@pytest.fixture
def stock_data(factory: FactoryProtocol) -> dict:
    return factory.stock_data()


@pytest.fixture
def stock(factory: FactoryProtocol, company_point: Point) -> dict:
    return factory.stock(point=company_point)


@pytest.fixture
def material_type(factory: FactoryProtocol) -> MaterialType:
    return factory.material_type()


@pytest.fixture
def material_type_data(factory: FactoryProtocol) -> dict:
    return factory.material_type_data()


@pytest.fixture
def material(factory: FactoryProtocol) -> dict:
    return factory.material()


@pytest.fixture
def stock_material(factory: FactoryProtocol, stock: Stock) -> StockMaterial:
    return factory.stock_material(stock=stock)
