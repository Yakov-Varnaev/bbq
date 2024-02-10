from typing import Any, Callable, Generic, Protocol, TypeVar

from mypy_extensions import Arg, KwArg
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


class ExistCheckAssertion(Protocol):
    def __call__(self, model: type[Model], **filter: Any) -> None:
        ...


ModelData = TypeVar("ModelData")


class GenericModelAssertion(Generic[ModelData]):
    def __call__(self, data: ModelData, **extra: Any) -> None:
        ...


ExistCheckAssertion = Callable[[Arg(type[Model], "model"), KwArg()], None]  # noqa: F821
