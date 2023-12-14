import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf

from app.testing import ApiClient
from app.testing.factory import FixtureFactory
from companies.models import Company
from companies.models.department import Department
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


@pytest.fixture
def stock_data(factory: FixtureFactory) -> dict:
    return factory.stock_data()


@pytest.fixture
def stock(factory: FixtureFactory, company_point: Point) -> dict:
    return factory.stock(point=company_point)
