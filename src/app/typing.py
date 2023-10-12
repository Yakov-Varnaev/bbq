from typing import Callable

from mypy_extensions import Arg, KwArg
from rest_framework.serializers import BaseSerializer

from django.db.models import Model, QuerySet

RestPageAssertion = Callable[
    [
        dict,
        QuerySet | list[Model],
        type[BaseSerializer],
        str | None,
        str | None,
    ],
    None,
]
ExistCheckAssertion = Callable[[Arg(type[Model], "model"), KwArg()], None]  # noqa: F821
ModelAssertion = Callable[[Arg(dict, "data"), KwArg()], None]  # noqa: F821
