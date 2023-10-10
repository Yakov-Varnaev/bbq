import pytest
from collections.abc import Callable

from django.db.models import Model

from app.models import DefaultModel


@pytest.fixture
def assert_doesnt_exist() -> Callable:
    def _assert(model: type[DefaultModel], **filter: dict) -> None:
        assert not model.objects.filter(**filter).exists()  # type: ignore[attr-defined]

    return _assert


@pytest.fixture
def assert_exists() -> Callable:
    def _assert(model: type[Model], **filter: dict) -> None:
        assert model.objects.filter(**filter).exists()  # type: ignore[attr-defined]

    return _assert
