import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf

from app.testing.factory import FixtureFactory
from companies.models.point import Point


@pytest.fixture
def employee_data_with_one_department(factory: FixtureFactory) -> dict[str, Any]:
    return factory.employee_data()


@pytest.fixture
def employee_data_with_several_departments(factory: FixtureFactory, company_point: Point) -> dict[str, Any]:
    return factory.employee_data(departments=factory.cycle(3).department(point=company_point))


@pytest.fixture(params=[lf("employee_data_with_one_department"), lf("employee_data_with_several_departments")])
def employee_data(request: pytest.FixtureRequest) -> dict[str, Any]:
    return request.param


@pytest.fixture
def employee_with_non_existing_user(factory: FixtureFactory) -> dict:
    return factory.employee_data(user=999)


@pytest.fixture
def employee_with_duplicating_department(factory: FixtureFactory) -> dict:
    department = factory.department()
    return factory.employee_data(departments=[department, department])


@pytest.fixture
def employee_with_non_existing_department(factory: FixtureFactory) -> dict:
    return factory.employee_data(departments=[999])


@pytest.fixture(
    params=[
        lf("employee_with_duplicating_department"),
        lf("employee_with_non_existing_user"),
    ]
)
def employee_invalid_data(request: pytest.FixtureRequest) -> dict:
    return request.param
