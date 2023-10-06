import mimesis
from mimesis import Field, Fieldset, Generic, Schema
from mimesis.locales import Locale
from mixer.backend.django import mixer

__all__ = ["mixer", "mimesis", "generic", "field", "fieldset", "Schema"]

generic = Generic(locale=Locale.EN)
field = Field(locale=Locale.EN)
fieldset = Fieldset(locale=Locale.EN)


def _random_user_name() -> str:
    return generic.person.username()


def _random_email() -> str:
    return generic.person.email()


mixer.register("users.User", username=_random_user_name, email=_random_email)
