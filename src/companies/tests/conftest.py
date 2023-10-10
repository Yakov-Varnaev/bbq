import pytest
from typing import Callable

from companies.models import Company, Point


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
def assert_company_point() -> Callable[[dict], None]:
    def _assert_company_point(data: dict, **extra: dict) -> None:
        point = Point.objects.get(address=data["address"])
        for key, value in {**data, **extra}.items():
            assert getattr(point, key) == value

    return _assert_company_point
