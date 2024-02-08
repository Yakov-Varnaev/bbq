import pytest
from typing import Any

from app.types import GenericModelAssertion
from users.models import User
from users.types import UserData


class DefaultUserAssert(GenericModelAssertion[UserData]):
    def check_superuser(self, user: User) -> None:
        ...

    def __call__(self, data: UserData, **extra: Any) -> User:
        merged_data = data | extra
        user_id = merged_data["id"]
        assert isinstance(user_id, int)
        user = User.objects.get(id=user_id)
        assert user.is_active
        self.check_superuser(user)

        for key, value in merged_data.items():
            assert getattr(user, key) == value, f"{key} is not {value} but {getattr(user, key)}"


class UserAssert(DefaultUserAssert):
    def check_superuser(self, user: User) -> None:
        assert not user.is_superuser
        assert not user.is_staff


class SuperuserAssert(DefaultUserAssert):
    def check_superuser(self, user: User) -> None:
        assert user.is_superuser
        assert user.is_staff


@pytest.fixture
def assert_user() -> GenericModelAssertion:
    return UserAssert()


@pytest.fixture
def assert_superuser() -> GenericModelAssertion:
    return SuperuserAssert()
