import pytest

from app.testing import ApiClient
from app.testing.factory import FixtureFactory
from companies.models import Company
from users.models import User


@pytest.fixture
def company(factory: FixtureFactory) -> Company:
    return factory.company()


@pytest.fixture
def company_owner(company: Company) -> User:
    return company.owner


@pytest.fixture
def as_company_owner(company_owner: User) -> ApiClient:
    return ApiClient(company_owner)


@pytest.fixture
def company_data(factory: FixtureFactory) -> dict:
    return factory.company_data()
