import pytest
from typing import Callable

from a12n.factory import UserData
from users.models import User


@pytest.fixture
def assert_user() -> Callable:
    def _assert_user(email: str, expected: UserData) -> None:
        user = User.objects.get(email=email)

        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, field_value in expected.items():
            assert getattr(user, field_name) == field_value

    return _assert_user
