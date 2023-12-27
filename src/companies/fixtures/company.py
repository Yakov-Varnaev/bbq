import pytest

from app.testing import ApiClient
from app.testing.factory import FixtureFactory
from companies.models import Company
from users.models import User


@pytest.fixture
def company(factory: FixtureFactory) -> Company:
    return factory.company()


@pytest.fixture
def company_pk(company: Company) -> int:
    return company.pk


@pytest.fixture
def another_company(factory: FixtureFactory) -> Company:
    return factory.company()


@pytest.fixture
def company_owner(company: Company) -> User:
    return company.owner


@pytest.fixture
def another_company_owner(another_company: Company) -> User:
    return another_company.owner


@pytest.fixture
def as_company_owner(company_owner: User) -> ApiClient:
    return ApiClient(company_owner)


@pytest.fixture
def as_another_company_owner(another_company_owner: User) -> ApiClient:
    return ApiClient(another_company_owner)


@pytest.fixture
def company_data(factory: FixtureFactory) -> dict:
    return factory.company_data()
