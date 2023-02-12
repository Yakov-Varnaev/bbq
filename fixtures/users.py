import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def token_creator(user_to_auth):
    token = RefreshToken.for_user(user_to_auth)
    return {'refresh': str(token), 'access': str(token.access_token)}


def token_authentication(client_to_auth, auth_token):
    client_to_auth.credentials(HTTP_AUTHORIZATION=f'JWT {auth_token["access"]}')
    return client_to_auth


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def unauthorized_client():
    return APIClient()


@pytest.fixture
def user():
    return mixer.blend(User)


@pytest.fixture
def unauthorized_user():
    return mixer.blend(User)


@pytest.fixture
def user_token(user):
    return token_creator(user)


@pytest.fixture
def unauthorized_user_token(unauthorized_user):
    return token_creator(unauthorized_user)


@pytest.fixture
def auth_client(client, user_token):
    return token_authentication(client, user_token)


@pytest.fixture
def auth_unauthorized_client(unauthorized_client, unauthorized_user_token):
    return token_authentication(unauthorized_client, unauthorized_user_token)
