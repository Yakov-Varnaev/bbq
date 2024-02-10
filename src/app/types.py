from typing import Any, Generic, Protocol, TypeVar

from rest_framework.serializers import BaseSerializer

from django.db.models import Model, QuerySet


class RestPageAssertion(Protocol):
    def __call__(
        self,
        page_data: dict,
        queryset: QuerySet[Model] | list[Model],
        serializer_class: type[BaseSerializer],
        next_link: str | None = None,
        previous_link: str | None = None,
    ) -> None:
        ...


_Model = TypeVar("_Model")


class GenericExistCheckAssertion(Generic[_Model]):
    def __call__(self, model: _Model, **filter: Any) -> None:
        ...


ModelData = TypeVar("ModelData")


class GenericModelAssertion(Generic[ModelData]):
    def __call__(self, data: ModelData, **extra: Any) -> None:
        ...
