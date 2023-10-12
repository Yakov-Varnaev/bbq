import pytest
from typing import Any, Callable

from pytest_lazyfixture import lazy_fixture as lf

from app.testing.api import ApiClient
from companies.models import Company, Point
from companies.models.department import Department


@pytest.fixture
def assert_company() -> Callable[[dict], None]:
    def _assert_company(data: dict, **extra: dict) -> None:
        company = Company.objects.get(name=data["name"])
        for key, value in {**data, **extra}.items():
            assert getattr(company, key) == value

    return _assert_company


@pytest.fixture
def assert_company_doesnt_exist() -> Callable:
    def _assert(**filter):
        assert not Company.objects.filter(**filter).exists()

    return _assert


@pytest.fixture
def assert_company_point() -> Callable[[dict, dict], None]:
    def _assert_company_point(data: dict, **extra: dict) -> None:
        point = Point.objects.get(address=data["address"])
        for key, value in {**data, **extra}.items():
            assert getattr(point, key) == value

    return _assert_company_point


@pytest.fixture
def assert_department() -> Callable[[dict, dict], None]:
    def _assert_department(data: dict[str, Any], **extra: dict[str, Any]):
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
