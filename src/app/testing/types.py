from typing import Protocol

from mimesis import Field, Fieldset, Generic, Schema
from mixer.backend.django import mixer


class FixtureFactory(Protocol):
    mixer: mixer
    schema: type[Schema]
    generic: Generic
    field: Field
    fieldset: Fieldset


__all__ = [
    "FixtureFactory",
]
