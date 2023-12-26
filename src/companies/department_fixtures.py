import pytest
from typing import Any

from app.testing.factory import FixtureFactory
from companies.models.department import Department
from companies.models.point import Point


@pytest.fixture
def department(factory: FixtureFactory, company_point: Point) -> Department:
    return factory.department(point=company_point)


@pytest.fixture
def department_data(factory: FixtureFactory) -> dict[str, Any]:
    return factory.department_data()


@pytest.fixture
def department_pk(department: Department) -> int:
    return department.pk
