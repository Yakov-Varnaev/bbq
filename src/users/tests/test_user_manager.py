import pytest
from collections.abc import Callable

from django.contrib.auth import get_user_model

from a12n.factory import RegistrationData, UserData

User = get_user_model()

pytestmark = [pytest.mark.django_db]


def test_user_manager_doesnt_require_username(
    registration_data: RegistrationData,
    expected_user_data: UserData,
    assert_user: Callable,
):
    user = User.objects.create_user(**registration_data)  # type: ignore[arg-type]

    assert user is not None
    assert_user(registration_data["email"], expected_user_data)


def test_user_manager_requires_email(
    registration_data: RegistrationData,
):
    del registration_data["email"]

    with pytest.raises(TypeError):
        User.objects.create_user(**registration_data)  # type: ignore[arg-type]


def test_user_manager_create_superuser(
    registration_data: RegistrationData,
    expected_user_data: UserData,
    assert_superuser: Callable,
):
    user = User.objects.create_superuser(**registration_data)  # type: ignore[arg-type]

    assert user is not None
    assert_superuser(registration_data["email"], expected_user_data)
    assert user.is_staff is True
    assert user.is_superuser is True
