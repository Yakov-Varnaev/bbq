import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf

from django.contrib.auth import get_user_model

from app.testing.api import ApiClient
from app.types import ModelAssertion
from companies.models import Company, Department, Employee, Point
from companies.models.stock import StockMaterial

User = get_user_model()


@pytest.fixture
def assert_company() -> ModelAssertion:
    def _assert_company(data: dict, **extra: Any) -> None:
        company = Company.objects.get(name=data["name"])
        for key, value in {**data, **extra}.items():
            assert getattr(company, key) == value

    return _assert_company


@pytest.fixture
def assert_company_point() -> ModelAssertion:
    def _assert_company_point(data: dict, **extra: Any) -> None:
        point = Point.objects.get(address=data["address"])
        for key, value in {**data, **extra}.items():
            assert getattr(point, key) == value

    return _assert_company_point


@pytest.fixture
def assert_department() -> ModelAssertion:
    def _assert_department(data: dict, **extra: Any) -> None:
        department = Department.objects.get(name=data["name"])
        for field_name, expected_value in (data | extra).items():
            assert getattr(department, field_name) == expected_value

    return _assert_department


@pytest.fixture
def assert_employee() -> ModelAssertion:
    def _assert_employee(data: dict, **extra: Any) -> None:
        employee = Employee.objects.get(user_id=data["user"])
        assert sorted([d.id for d in employee.departments.all()]) == sorted(data.pop("departments"))
        assert employee.user.id == data.pop("user")

        for field_name, expected_value in (data | extra).items():
            assert getattr(employee, field_name) == expected_value

    return _assert_employee


@pytest.fixture
def assert_stock_material() -> ModelAssertion:
    def _assert_stock_material(data: dict, **extra: Any) -> None:
        stock_material = StockMaterial.objects.get(material_id=data["material"])
        assert stock_material.material.id == data.pop("material")

        for field_name, expected_value in (data | extra).items():
            assert getattr(stock_material, field_name) == expected_value

    return _assert_stock_material


@pytest.fixture(
    params=[
        lf("as_anon"),
        lf("as_user"),
        lf("as_company_owner"),
        lf("as_another_company_owner"),
    ],
)
def reader_client(request) -> ApiClient:
    return request.param


@pytest.fixture(
    params=[
        lf("as_company_owner"),
    ]
)
def as_point_managing_staff(request) -> ApiClient:
    return request.param
