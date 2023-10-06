from typing import Protocol

from mimesis import Field, Fieldset, Generic, Schema
from mixer.backend.django import mixer


class FactoryProtocol(Protocol):
    mixer: mixer
    schema: Schema
    generic: Generic
    field: Field
    fieldset: Fieldset


__all__ = [
    "FactoryProtocol",
]
