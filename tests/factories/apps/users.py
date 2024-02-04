from django.contrib.auth.models import AnonymousUser

from app.testing import register
from app.testing.factory import FixtureFactory
from users.models import User


@register
def user(self: FixtureFactory, **kwargs: dict) -> User:
    return self.mixer.blend("users.User", **kwargs)


@register
def anon(self: FixtureFactory, **kwargs: dict) -> AnonymousUser:
    return AnonymousUser()


@register
def superuser(self: FixtureFactory, **kwargs: dict) -> User:
    return self.mixer.blend("users.User", is_superuser=True, **kwargs)
