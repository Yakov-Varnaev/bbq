import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return mixer.blend(User)


@pytest.fixture
def user_token(user):
    token = RefreshToken.for_user(user)
    return {'refresh': str(token), 'access': str(token.access_token)}


@pytest.fixture
def auth_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'JWT {user_token["access"]}')
    return client
