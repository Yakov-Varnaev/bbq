import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def auth_setup(auth_client):
    """
    This fixture creates an additional user with it's APIClient to test expected CRUD permissions.

    Returns
    -------

    authorized_client - APIClient of user with expected CREATE, READ, UPDATE, DELETE permissions
    auth_client - APIClient of user with expected CREATE, READ permissions
    """

    authorized_user = mixer.blend(User)
    authorized_user_token = RefreshToken.for_user(authorized_user).access_token

    authorized_client = APIClient()
    authorized_client.credentials(HTTP_AUTHORIZATION=f'JWT {authorized_user_token}')

    return authorized_client, auth_client
