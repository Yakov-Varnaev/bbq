import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def auth_setup(db, auth_client):

    authorized_user = mixer.blend(User)
    authorized_user_token = RefreshToken.for_user(authorized_user).access_token

    authorized_client = APIClient()
    unauthorized_client = auth_client

    authorized_client.credentials(HTTP_AUTHORIZATION=f'JWT {authorized_user_token}')

    return authorized_client, unauthorized_client
