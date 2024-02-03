import pytest

from app.testing.factory import FixtureFactory
from companies.models import Company
from companies.models.point import Point


@pytest.fixture
def company_point(factory: FixtureFactory, company: Company) -> dict:
    return factory.company_point(company=company)


@pytest.fixture
def company_point_pk(company_point: Point) -> int:
    return company_point.pk


@pytest.fixture
def company_point_data(factory: FixtureFactory) -> dict:
    return factory.company_point_data()
