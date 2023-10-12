import pytest
from collections.abc import Callable

from rest_framework.serializers import BaseSerializer

from django.db.models import QuerySet


@pytest.fixture
def assert_rest_page() -> Callable[[dict, QuerySet, type[BaseSerializer], None | str, None | str], None]:
    def _assert_rest_page(
        page_data: dict,
        queryset: QuerySet,
        serializer_class: type[BaseSerializer],
        next_link: None | str = None,
        previous_link: None | str = None,
    ) -> None:
        assert page_data["count"] == len(queryset)
        assert page_data["next"] == next_link
        assert page_data["previous"] == previous_link
        assert page_data["results"] == serializer_class(queryset, many=True).data

    return _assert_rest_page
