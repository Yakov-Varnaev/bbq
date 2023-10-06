import pytest
from typing import Callable

from companies.models import Company


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
