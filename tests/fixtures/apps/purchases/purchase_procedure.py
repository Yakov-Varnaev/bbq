import pytest

from app.testing.factory import FixtureFactory
from companies.models import Procedure
from purchases.models import Purchase, PurchaseProcedure
from purchases.types import PurchaseProcedureData


@pytest.fixture
def purchase_procedure_data(factory: FixtureFactory) -> PurchaseProcedureData:
    return factory.purchase_procedure()


@pytest.fixture
def purchase_procedure(factory: FixtureFactory, procedure: Procedure, purchase: Purchase) -> PurchaseProcedure:
    return factory.purchase_procedure(procedure=procedure, purchase=purchase)
