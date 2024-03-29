import pytest
from typing import Any

from rest_framework.serializers import BaseSerializer

from django.db.models import Model, QuerySet

from app.types import GenericExistCheckAssertion, RestPageAssertion


@pytest.fixture
def assert_rest_page() -> RestPageAssertion:
    def _assert_rest_page(
        page_data: dict,
        queryset: QuerySet[Model] | list[Model],
        serializer_class: type[BaseSerializer],
        next_link: str | None = None,
        previous_link: str | None = None,
    ) -> None:
        assert page_data["count"] == len(queryset)
        assert page_data["next"] == next_link
        assert page_data["previous"] == previous_link
        assert page_data["results"] == serializer_class(queryset, many=True).data

    return _assert_rest_page


class NonExistCheckAssertion(GenericExistCheckAssertion[Model]):
    def __call__(self, model: Model, **filter: Any) -> None:
        assert not model.objects.filter(**filter).exists()  # type: ignore[attr-defined]


class ExistCheckAssertion(GenericExistCheckAssertion[Model]):
    def __call__(self, model: Model, **filter: Any) -> None:
        assert model.objects.filter(**filter).exists()  # type: ignore[attr-defined]


@pytest.fixture
def assert_doesnt_exist() -> GenericExistCheckAssertion:
    return NonExistCheckAssertion()


@pytest.fixture
def assert_exists() -> GenericExistCheckAssertion:
    return ExistCheckAssertion()
