import pytest
from typing import Callable

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from tests.factories.apps.a12n import RegistrationData, UserData

pytestmark = [
    pytest.mark.django_db,
]


def test_registration(
    as_anon: ApiClient,
    registration_data: RegistrationData,
    expected_user_data: UserData,
    assert_user: Callable,
):
    as_anon.post(reverse("api_v1:a12n:user-list"), data=registration_data)  # type: ignore

    assert_user(registration_data["email"], expected_user_data)


def test_registration_invalid_data(factory: FixtureFactory):
    pass


def test_registration_duplicate_email():
    pass
