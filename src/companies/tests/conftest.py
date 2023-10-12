import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf

from app.testing.api import ApiClient
from app.typing import ModelAssertion
from companies.models import Company, Point
from companies.models.department import Department


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
