import pytest
from typing import Any

from app.testing.factory import FixtureFactory
from companies.models import Category, Department, Point, Procedure


@pytest.fixture
def department(factory: FixtureFactory, company_point: Point) -> Department:
    return factory.department(point=company_point)


@pytest.fixture
def department_data(factory: FixtureFactory) -> dict[str, Any]:
    return factory.department_data()


@pytest.fixture
def category_data(factory: FixtureFactory) -> dict:
    return factory.category_data()


@pytest.fixture
def category(factory: FixtureFactory) -> Category:
    return factory.category()


@pytest.fixture
def procedure(factory: FixtureFactory, category: Category, department: Department) -> Procedure:
    return factory.procedure(category=category, department=department)


@pytest.fixture
def procedure_data(factory: FixtureFactory, category: Category) -> dict[str, Any]:
    return factory.procedure_data(category=category.id)


@pytest.fixture
def procedure_reverse_kwargs(department: Department) -> dict[str, Any]:
    return {
        "company_pk": department.point.company.id,
        "point_pk": department.point.id,
        "department_pk": department.id,
    }
