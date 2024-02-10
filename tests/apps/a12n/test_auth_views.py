import pytest

from django.urls import reverse

from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.types import GenericModelAssertion
from users.types import RegistrationData, UserData

pytestmark = [
    pytest.mark.django_db,
]


def test_registration(
    as_anon: ApiClient,
    registration_data: RegistrationData,
    expected_user_data: UserData,
    assert_user: GenericModelAssertion[UserData],
):
    response = as_anon.post(reverse("api_v1:a12n:user-list"), data=registration_data)  # type: ignore

    assert_user(expected_user_data, id=response["id"])


def test_registration_invalid_data(factory: FixtureFactory):
    pass


def test_registration_duplicate_email():
    pass
