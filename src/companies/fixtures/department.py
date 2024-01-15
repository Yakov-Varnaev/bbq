import pytest
from typing import Any

from app.testing.factory import FixtureFactory
from companies.models import Department, MaterialType, Point, Procedure


@pytest.fixture
def department(factory: FixtureFactory, company_point: Point) -> Department:
    return factory.department(point=company_point)


@pytest.fixture
def department_data(factory: FixtureFactory) -> dict[str, Any]:
    return factory.department_data()


@pytest.fixture
def department_pk(department: Department) -> int:
    return department.pk


@pytest.fixture
def procedure(factory: FixtureFactory, material_type: MaterialType, department: Department) -> Procedure:
    return factory.procedure(kind=material_type, department=department)


@pytest.fixture
def procedure_data(factory: FixtureFactory) -> dict[str, Any]:
    return factory.procedure_data()
