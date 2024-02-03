import pytest

from app.testing.factory import FixtureFactory
from users.models import User


@pytest.fixture
def user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture
def another_user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture
def superuser(factory: "FixtureFactory") -> User:
    return factory.superuser()


@pytest.fixture
def another_user_id(another_user: User) -> int:
    """
    This is usefull for testing endpoints, which handle serializers with owner/author fields.
    """
    return another_user.pk
