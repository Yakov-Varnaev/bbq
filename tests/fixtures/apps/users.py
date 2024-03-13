import pytest

from app.testing.factory import FixtureFactory
from users.models import User


@pytest.fixture
def user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture
def superuser(factory: "FixtureFactory") -> User:
    return factory.superuser()
