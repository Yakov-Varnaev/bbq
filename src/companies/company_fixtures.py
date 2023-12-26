import pytest

from app.testing import ApiClient
from app.testing.factory import FixtureFactory
from companies.models import Company
from companies.models.point import Point
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


@pytest.fixture
def company_point(factory: FixtureFactory, company: Company) -> dict:
    return factory.company_point(company=company)


@pytest.fixture
def company_point_pk(company_point: Point) -> int:
    return company_point.pk


@pytest.fixture
def company_point_data(factory: FixtureFactory) -> dict:
    return factory.company_point_data()
