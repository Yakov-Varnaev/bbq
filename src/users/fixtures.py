import pytest
from typing import TYPE_CHECKING, Callable

from a12n.factory import UserData
from users.models import User

if TYPE_CHECKING:
    from app.testing.factory import FixtureFactory


@pytest.fixture
def user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture
def another_user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture
def another_user_id(another_user: User) -> int:
    """
    This is usefull for testing endpoints, which handle serializers with owner/author fields.
    """
    return another_user.pk


def __asert_user(user: User, expected: UserData) -> None:
    assert user.id
    assert user.is_active

    for field_name, field_value in expected.items():
        assert getattr(user, field_name) == field_value


@pytest.fixture
def assert_user() -> Callable:
    def _assert_user(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        __asert_user(user, expected)

        assert not user.is_superuser
        assert not user.is_staff

    return _assert_user


@pytest.fixture
def assert_superuser() -> Callable:
    def _assert_superuser(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)
        __asert_user(user, expected)
        assert user.is_superuser
        assert user.is_staff

    return _assert_superuser
