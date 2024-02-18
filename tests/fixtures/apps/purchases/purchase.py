import pytest

from app.testing.factory import FixtureFactory
from purchases.models import Purchase
from purchases.types import PurchaseData


@pytest.fixture
def purchase_data(factory: FixtureFactory) -> PurchaseData:
    return factory.purchase_data()


@pytest.fixture
def purchase(factory: FixtureFactory) -> Purchase:
    return factory.purchase()
