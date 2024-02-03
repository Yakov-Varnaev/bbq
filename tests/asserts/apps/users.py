import pytest

from typing_extensions import Callable

from tests.factories.apps.a12n import UserData
from users.models import User


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
